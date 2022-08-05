import os

import inject
from flask import Flask

from src.adapters.database.postgres import PostgresAdapter
from src.domain.database_interface import DatabaseInterface


def configure_application(application: Flask) -> None:
    application.config.update(
        DATABASE_URI=os.getenv('DATABASE_URI')
    )


def configure_inject(application: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, PostgresAdapter(application.config['DATABASE_URI']))

    inject.configure(config)


def configure_profiler(application: Flask) -> None:
    application.config["flask_profiler"] = {
        "enabled": application.config['DEBUG'],
        "storage": {
            "engine": "sqlalchemy",
            "db_url": application.config['DATABASE_URI']
        },
        "basicAuth": {
            "enabled": True,
            "username": "admin",
            "password": "admin"
        },
        "ignore": [
            "^/static/.*"
        ]
    }
