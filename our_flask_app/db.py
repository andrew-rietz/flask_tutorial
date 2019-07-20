import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    """Create the connection to the database"""
    if "db" not in g:
        # g is a special object that is unique for each request
        # It stores data that may be accessed by multiple functions
        # during the request. If get_db is called a second time,
        # the connection is stored and reused instead of creating
        # a new connection
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )

        # This tells the connection to return rows that behave
        # like dicts, allowing access to columns by name
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Close the database connection
    >>> Must be registered with the application instance,
    otherwise can't be used by the application
    (because we're using an application factory)
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """Initialize the database"""
    db = get_db()

    # open_resource() opens a file relative to `our_flask_app`
    # package
    with current_app.open_resource("schema.sql") as sql_schema:
        db.executescript(sql_schema.read().decode("utf8"))

# click.command() defines a command line command called 'init-db'
# that calls the init_function and returns a success message
@click.command("init-db")
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables.
    >>> Must be registered with the application instance,
    otherwise can't be used by the application
    (because we're using an application factory)
    """
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """
    Registers functions with the application
    >>> Import and call this function from our application factory
    """
    # app.teardown_appcontext() tells flask to call that function
    # when cleaning up after returning the reponse
    app.teardown_appcontext(close_db)
    # app.cli.add_command() adds a new command that can be called
    # with the `flask` command
    app.cli.add_command(init_db_command)
