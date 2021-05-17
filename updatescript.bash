#!/usr/bin/env bash

cd "$(dirname $0)"
git pull --quiet
python3 updatehtml.py
git commit -am "update at $(date)" --quiet
git push --quiet
