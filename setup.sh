#!/bin/sh

# psycopg2 fails to install on my machine without manually specifying LDFLAGS for openssl
# using fish shell, for me that's `set -gx LDFLAGS "-L/usr/local/opt/openssl/lib"`
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Run the database migrations!"
echo "python manage.py db create && python manage.py db migrate"
echo "python manage.py db create test && python manage.py db migrate test"
