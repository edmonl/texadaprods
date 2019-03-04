import sqlite3
from contextlib import contextmanager

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


@contextmanager
def cursor():
    db = get()
    try:
        cur = db.cursor()
        yield cur
    except:
        db.rollback()
        raise
    else:
        db.commit()
    finally:
        cur.close()


def close(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close)
    app.cli.add_command(init_db_cmd)


@click.command('init-db')
@with_appcontext
def init_db_cmd():
    """Import database schema."""
    with cursor() as cur, current_app.open_resource('schema.sql') as f:
        cur.executescript(f.read().decode('utf8'))
    close()
    click.echo('Initialized the database.')
