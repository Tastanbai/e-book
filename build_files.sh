#!/bin/bash
echo "Where is Python:"
which python
echo "Python Version:"
python --version
echo "Where is Pip:"
which pip
echo "Pip Version:"
pip --version

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
