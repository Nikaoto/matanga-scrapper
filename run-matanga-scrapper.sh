#! /usr/bin/env bash
cd /home/nika/matanga-scrapper
DATA_DIR="data"
NOW_MONTH="$(date +%m)"
SAVE_DIR="${DATA_DIR}/${NOW_MONTH}"
mkdir -p "$SAVE_DIR"
xvfb-run python3 scrape.py "$SAVE_DIR"
