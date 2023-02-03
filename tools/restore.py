#!./venv/bin/python
import sys
from datetime import date, timedelta
from pathlib import Path

import boto3
from dotenv import dotenv_values

config = dotenv_values(".env")

s3 = boto3.resource(
    "s3",
    endpoint_url=config["BACKUP_ENDPOINT"],
    aws_access_key_id=config["BACKUP_ACCESS_KEY"],
    aws_secret_access_key=config["BACKUP_SECRET_KEY"],
    aws_session_token=None,
    config=boto3.session.Config(signature_version="s3v4"),
)


def main(cutoff, *search_args):
    search_args = [a.lower() for a in search_args]
    b = s3.Bucket(config["BACKUP_BUCKET"])
    for days in range(cutoff):
        prefix = date.today() - timedelta(days=days)
        print(f"Looking for files from {prefix}...")
        prefix = str(prefix)
        for obj in b.objects.filter(Prefix=prefix):
            key = obj.key.lower()
            if all(a in key for a in search_args):
                print(f"  Found {obj.key}")
                p = Path(config["LOGS_DIR"]) / "archive" / obj.key
                print(f"    Downloading to {p}")
                with p.open("wb") as fp:
                    b.download_fileobj(obj.key, fp)


if __name__ == "__main__":
    cutoff = 7
    if len(sys.argv) > 1:
        cutoff = int(sys.argv[1])
    main(cutoff, *sys.argv[2:])
