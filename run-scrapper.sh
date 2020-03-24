#! /usr/bin/env bash
DATA_DIR="data"
NOW_MONTH="$(date +%m)"
SAVE_DIR="${DATA_DIR}/${NOW_MONTH}"
mkdir -p "$SAVE_DIR"
xvfb-run python3 test.py "$SAVE_DIR"
