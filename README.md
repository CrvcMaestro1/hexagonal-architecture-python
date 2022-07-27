 Hexagonal Architecture example in Python using Flask and SqlAlchemy
=====================================================================

------------------------
 Installation and Usage
------------------------

## Requirements
- Install Python 3.7 or 3.10, then
```bash
$ pip install virtualenv
$ sudo apt-get install libpq-dev
$ git clone https://https://gitlab.com/crvc1998/hexagonal-architecture-python.git
$ cd hexagonal-architecture-python
```

## Running the database
To use a local database:
```bash
# Run only the first time
$ mkdir docker/db
```

### Run docker compose
```bash
$ docker-compose up -d
```

## 

## To run

```bash
$ py -m venv venv
$ source venv/bin/activate
$ chmod +x ./setup.sh
$ ./setup.sh
$ python manage.py db create
$ python manage.py db migrate
$ python manage.py server
```
To run the tests:

```bash
$ python manage.py db create test
$ python manage.py db migrate test
$ python manage.py check tests
``` 
------------------------
 Thanks to Alex Grover's post
------------------------
https://alexgrover.me/posts/python-hexagonal-architecture
