#!/bin/bash
which python
which pip
pip install -r requirements.txt
python manage.py collectstatic --no-input