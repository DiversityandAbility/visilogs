#!/bin/sh
set -eu

mkdir -p ./logs/fresh ./logs/archive

python3 -m venv venv

. venv/bin/activate

pip install visidata==2.11