#!/bin/bash
virtualenv venv &&
. venv/bin/activate &&
pip install -r pip-requirements.txt
