#!/bin/bash
cd source && 
../venv/bin/python manage.py test --liveserver=pybook-staging.lazerstorm.com
