#!/bin/sh
set -eu

set -a; . ./.env; set +a

cat "$LOGS_DIR"/*/*.log* | ./venv/bin/vd --filetype=jsonl --quitguard
