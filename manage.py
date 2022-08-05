import os
import subprocess
from typing import Union, List

import click
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def check_uri() -> bool:
    db_uri_check = os.getenv("DATABASE_URI")
    return db_uri_check is not None


def load_env(env: str) -> None:
    dotenv_file = '.env'
    if env != 'dev':
        dotenv_file = f'.env.{env}'
    load_dotenv(dotenv_file)


def validate_env(_context: click.Context, _parameter: Union[click.Option, click.Parameter],
                 env: str) -> str:
    values = ('dev', 'test')
    if env not in values:
        raise click.BadParameter(f'`env` must be one of: {values}')
    if not check_uri():
        load_env(env)
    return env


def run_sql(statements: List) -> None:
    conn = psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


@click.group('App server CLI')
def cli() -> None:
    pass


@cli.command(help='Run the web server')
def server() -> int:
    return subprocess.call(['flask', 'run'])


@cli.group(help="Manage the database")
def db() -> None:
    pass


@db.command(help="Create the database")
@click.argument('env', envvar='ENV', default='dev', callback=validate_env)
def create(env: str) -> None:
    click.echo(f'Creating database for `{env}` environment...')
    db_name = f'hex_{env}'
    try:
        run_sql([f"CREATE DATABASE {db_name}"])
    except psycopg2.errors.DuplicateDatabase:
        print(f"The database {db_name} already exists and will not be recreated")


@db.command(help="Run the database migrations")
@click.argument('env', envvar='ENV', default='dev', callback=validate_env)
def migrate(env: str) -> int:
    click.echo(f'Running migrations for `{env}` environment...')
    load_env(env)
    return subprocess.call(['alembic', 'upgrade', 'head'])


@cli.group(help='Run the code quality tools')
def check() -> None:
    pass


@check.command(help='Run the linter')
def style() -> int:
    click.echo('Running `flake8`...')
    return subprocess.call('flake8')


@check.command(help='Run the test suite')
def tests() -> int:
    click.echo('Running `pytest`...')
    return subprocess.call('pytest')


@check.command(help='Run the static analyzer')
def types() -> int:
    click.echo('Running `mypy`...')
    return subprocess.call('mypy')


if __name__ == "__main__":
    cli()
