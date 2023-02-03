#!/bin/sh
set -eu

set -a; . ./.env; set +a

rm "$LOGS_DIR"/archive/*
