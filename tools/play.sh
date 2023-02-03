#!/bin/sh
set -eu

set -a; . ./.env; set +a

cat "$LOGS_DIR"/*/*.log* | ./venv/bin/vd --play "$1"
