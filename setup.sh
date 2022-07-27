#!/bin/sh

# psycopg2 fails to install on my machine without manually specifying LDFLAGS for openssl
# using fish shell, for me that's `set -gx LDFLAGS "-L/usr/local/opt/openssl/lib"`
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "FLASK_APP=hex.application:create_application
FLASK_ENV=development
ENV=dev
DATABASE_URI=postgresql://postgres:postgres@db:5432/hex_dev
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_HOST=db
POSTGRES_DB=postgres
POSTGRES_PASSWORD=postgres
" > .env

echo "ENV=test
DATABASE_URI=postgresql://postgres:postgres@db:5432/hex_test
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_HOST=db
POSTGRES_DB=postgres
POSTGRES_PASSWORD=postgres
" > .env.test

echo "Run the database migrations!"
echo "python manage.py db create && python manage.py db migrate"
echo "python manage.py db create test && python manage.py db migrate test"
