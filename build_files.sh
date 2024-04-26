#!/bin/bash
#!/bin/bash
echo "Where is Python:"
which python
echo "Python Version:"
python --version
echo "Where is Pip:"
which pip
echo "Pip Version:"
pip --version

pip install -r requirements.txt
python manage.py collectstatic --no-input