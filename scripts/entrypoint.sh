#!/bin/bash

echo "Apply Database migrations"
python3 manage.py makemigrations --noinput
python3 manage.py migrate

echo "Loading test data"
python manage.py loaddata data.json

echo "Running team monitor server"
python3 manage.py runserver 0.0.0.0:8000
