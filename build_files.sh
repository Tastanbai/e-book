#!/bin/bash

# sudo apt-get install -y libmysqlclient-dev
python3 -m pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py collectstatic