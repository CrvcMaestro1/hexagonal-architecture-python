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

## Create .env file
In the files, there is a .env.example file, copy into .env file and change the values of variables
```bash
# Copy the .env.example
$ cp .env.example .env
```

## Running the database
To use a local database:
```bash
# Run only the first time
$ mkdir docker/db
```

### Run docker compose
```bash
$ docker-compose -f docker/docker-compose.yml up -d
```

## To run

```bash
$ py -m venv venv
$ source venv/bin/activate
$ chmod +x ./setup.sh
$ ./setup.sh
$ docker-compose -f docker/docker-compose.yml exec web bash
$ python manage.py db create # already executed in docker-compose file
$ python manage.py db migrate
$ python manage.py server # run the server (run flask without docker-compose)
```
To run the tests:

```bash
$ docker-compose -f docker/docker-compose.yml exec web bash
$ python manage.py db create test
$ python manage.py db migrate test
$ python manage.py check tests
``` 
------------------------
 Thanks to Alex Grover's post
------------------------
https://alexgrover.me/posts/python-hexagonal-architecture
