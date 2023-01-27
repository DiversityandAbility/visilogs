#!/bin/sh
set -eu

cat ./logs/*/*.log* | ./venv/bin/vd --filetype=jsonl --quitguard
