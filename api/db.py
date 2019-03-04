import sqlite3
from contextlib import contextmanager

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = lambda c, r: dict(zip((col[0] for col in c.description), r))
    return g.db


@contextmanager
def cursor():
    with get() as db:
        cur = db.cursor()
        yield cur
        cur.close()


def close(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_cmd)


def init_db():
    with cursor() as cur, current_app.open_resource('schema.sql') as f:
        cur.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    """Import database schema."""
    init_db()
    close()
    click.echo('Initialized the database.')
