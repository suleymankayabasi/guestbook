#!/bin/bash

echo "Create migrations"
python3 manage.py makemigrations guestbook
echo "=================================="

echo "Migrate"
python3 manage.py migrate
echo "=================================="

echo "Load Data"
python3 manage.py loaddata users.json
python3 manage.py loaddata entries.json



echo "Start server"
python3 manage.py runserver 0.0.0.0:8000