#!/usr/bin/env bash

cd "$(dirname $0)"
git pull
python3 updatehtml.py
git commit -am "update at $(date)"
git push