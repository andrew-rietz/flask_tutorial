import os

from flask import Flask


def create_app(test_config=None):
    """
    This file will contain the application factory
    The application factory sets any configuration, registration, and
    other setup the application needs. Then, the application is returned.
    """
    # create and configure the app
    # The app needs to know where it's located to set up some paths
    # Using __name__ is a convenient way to tell it that
    # We also tell the app that the instance folder is located outside
    # the package. This file will hold data that shouldn't be committed
    # to version control (secrets, database file, etc)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Secret key is set to 'dev' as a convenient value for development
        # change to a random and secure value for deployment
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "our_flask_app.sqlite")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # will override default config with values taken from our config.py file
        # for instance, can be used to set a real SECRET_KEY
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists - Flask doesn't create automaticalaly so
    # you need to tell it to be created
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Register the database with the application
    from . import db
    db.init_app(app)

    # Register the `auth` blueprint with the app
    from . import auth
    app.register_blueprint(auth.bp)

    return app
