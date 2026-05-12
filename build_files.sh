#!/bin/bash

echo "BUILD START"

# Create a virtual environment to avoid PEP 668 restriction
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Run database migrations
python manage.py migrate --noinput

echo "BUILD END"
