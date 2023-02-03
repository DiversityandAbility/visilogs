#!/bin/sh
set -eu

set -a; . ./.env; set +a

mkdir -p "$LOGS_DIR/fresh" "$LOGS_DIR/archive"

python3 -m venv venv

. venv/bin/activate

pip install visidata==2.11 boto3==1.26.58 python-dotenv==0.21.1