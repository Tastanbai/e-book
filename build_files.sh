#!/bin/bash
export PATH="/usr/bin/python:$PATH"
export PATH="$HOME/.local/bin:$PATH"
which python
which python3

# Проверка на наличие файла requirements.txt перед установкой зависимостей
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# Проверка на наличие manage.py перед выполнением Django команд
if [ -f "manage.py" ]; then
    python manage.py collectstatic --no-input
else
    echo "manage.py not found"
fi
