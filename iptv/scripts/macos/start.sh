#!/usr/bin/env bash
set -e

if [ -d venv ]
then
    python -m venv venv
fi

source ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python launch.py

deactivate