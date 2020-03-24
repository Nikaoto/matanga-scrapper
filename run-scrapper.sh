#! /usr/bin/env bash
NOW_MONTH="$(date +%m)"
mkdir -p "$NOW_MONTH"
xvfb-run python3 scrape.py "$NOW_MONTH"
