#!/bin/bash
. venv/bin/activate &&
cd source &&
python manage.py test
