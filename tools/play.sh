#!/bin/sh
set -eu

set -a; . ./.env; set +a

cat "$LOGS_DIR"/fresh/* "$LOGS_DIR"/archive/* | ./venv/bin/vd --play "$1"
