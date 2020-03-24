#! /usr/bin/env bash
cd /home/nika/matanga-scrapper
DATA_DIR="data"
LOGS_DIR="logs"
ERR_LOGS_DIR="logs"

NOW_MONTH="$(date +%m)"
SAVE_DIR="${DATA_DIR}/${NOW_MONTH}"
LOG_FILE="${LOGS_DIR}/${NOW_MONTH}.log"
ERR_LOG_FILE="${LOGS_DIR}/${NOW_MONTH}.errlog"

mkdir -p "$SAVE_DIR"
mkdir -p "$LOGS_DIR"

xvfb-run python3 scrape.py "$SAVE_DIR" 1>> "$LOG_FILE" 2>> "$ERR_LOG_FILE"
