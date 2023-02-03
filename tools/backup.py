#!./venv/bin/python
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import uuid

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


def find_old_log_files():
    cutoff = config.get("BACKUP_ARCHIVE_AFTER", 7)
    cutoff = date.today() - timedelta(days=int(cutoff))
    fresh_logs = Path(config["LOGS_DIR"]) / "fresh"
    for p in fresh_logs.iterdir():
        if p.is_file() and ".log" in p.name:
            mtime = p.stat().st_mtime
            mtime = datetime.fromtimestamp(mtime, tz=timezone.utc)
            mtime = mtime.date()
            if mtime <= cutoff:
                yield p, mtime


def rename(log_file, m_time):
    name = log_file.name.split(".")
    return ".".join(
        [
            str(m_time),
            name[0],
            str(uuid.uuid4()),
            "log",
        ]
    )


def main():
    for log_file, m_time in find_old_log_files():
        name = rename(log_file, m_time)
        print(f"Archiving {log_file} to {name}...")
        with log_file.open("rb") as fp:
            s3.Bucket(config["BACKUP_BUCKET"]).put_object(Key=name, Body=fp)
        print("  Deleting local file...")
        log_file.unlink()


if __name__ == "__main__":
    main()
