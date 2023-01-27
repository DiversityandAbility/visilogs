#!/bin/sh
set -eu

cat ./logs/*/*.log* | ./venv/bin/vd --play "$1"
