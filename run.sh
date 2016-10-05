#!/bin/bash
. venv/bin/activate &&
cd superlists &&
python manage.py runserver 9090
