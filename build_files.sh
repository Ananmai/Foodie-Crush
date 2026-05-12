#!/bin/bash

echo "BUILD START"

# Ensure pip is up to date and install dependencies
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

# Verify installation
python3.12 -c "import django; print('Django version:', django.get_version())"

# Collect static files
python3.12 manage.py collectstatic --noinput --clear

echo "BUILD END"
