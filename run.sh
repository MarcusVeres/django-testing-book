#!/bin/bash
. venv/bin/activate &&
cd source &&
python manage.py runserver 9090
