# flask_tutorial
Full tutorial available in flask documentation:
https://flask.palletsprojects.com/en/1.1.x/tutorial/

For this tutorial I created an app called **our_flask_app**. The tutorial uses
a SQLite database for simplicity.

## Table of Contents
1. [Application Setup](application-setup)
2. [Test Application Works](test-application-works)
3. [Define and Access Database](define-and-access-database)
4. [Blueprints and Views](blueprints-and-views)
5. [Templates](templates)


#### Application Setup
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)  
The most straightforward way to create a Flask application is to create a global
Flask instance directly at the top of your code. While this is simple and useful
in some cases, but can cause some  issues as the project grows.

Instead of creating a Flask instance globally, create it inside a function. This
function is known as the `application factory`. Any configuration, registration,
and other setup the application needs will happen inside the function, then the
application will be returned.  
[See `application factory`](our_flask_app/__init__.py)  


> Test Application Works

`export FLASK_APP=our_flask_app`  
`export FLASK_ENV=development`  
`flask run`


#### Define and Access Database
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/database/)  
> Connect to the database

Create a connection to the database. All queries and operations are
performed using the connection, and then the connection is closed
after the work is finished. Typically, the connection is created
during the request and closed before the request is sent.  
[See `db.py`](our_flask_app/db.py)

> Create the Tables

In SQLite, data is stored in tables and columns. These need to be
created before you can store and retrieve data. `our_flask_app` will
store users in a `user` table and posts in a `post` table.  
[See `schema.sql`](our_flask_app/schema.sql)

> Register with the Application

We need to register our functions with the application instance,
otherwise they can't be used by the application. Because we're using
a factory function, that instance isn't available when writing
the functions. Instead we need to write a function that takes an
application and does the registration.  
[See `db.py`](our_flask_app/db.py)

> Initialize the Database File

Now that `init-db` has been registerd with the app, it can be called
using the `flask` command, similar to the `flask run` command above.


#### Blueprints and Views
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/views/)  
A `view` function is the code you write to respond to requests to
your application. The view returns data that Flask turns into an
outgoing response. Flask can generate a URL to a view based on its
name and arguments, or Flask can match a view based on a URL that
is passed in.

A `blueprint` is a way to organize a group of unrelated views and
other code. Views are registered with a blueprint, and the blueprint
is then registered with the application when it is available in the
factory function.

> Create a Blueprint

Our app will have two blueprints. One for authentication functions
and one for blog post functions. The code for each will go in a
separate module. The blog needs to know about authentication so
we'll write the authentication blueprint first.  
[See `auth`](our_flask_app/auth.py)


#### Add views to the Blueprint
The authentication blueprint will have views to register new users
and to log in and log out.
> View 1: Register

When the user visits `/auth/register`, the `register` view will
return HTML with a form for them to fill out, validate their input
and either show the form again with an error (invalid input) or
create the new user and go to the login page.

The view performs the backend logic, and serves HTML to the user.  
[See `auth`](our_flask_app/auth.py)

> View 2: Login

When the user visits `/auth/login`, the `login` view will
return HTML with a form for them to fill out, validate their input
and either show the form again with an error (invalid input) or
log the user in and store their data in the `session`. Data stored in the `session` is available for future requests.  
[See `auth`](our_flask_app/auth.py)

> View 3: Logout

When the user logs out, their data is removed from the `session`.
The user is returned to the site index.  
[See `auth`](our_flask_app/auth.py)

> Require Authentication in Other Views

Creating, editing, and deleting blog posts will require a user to
be logged in. A decorator `login_required` can be used to check
this for each view it's applied to. This will be used in the
blog views.  
[See `auth`](our_flask_app/auth.py)

> Endpoints and URLs

The `url_for()` function generates the URL to a view based on a
name and arguments. The name associated with a view is also called
the `endpoint`. By default, the `endpoint` has the same name as the
name of the view function.

When using a blueprint, the name of the blueprint is prepended to
the name of the function.

Example usage without blueprint:  
`url_for("hello")`  
Example usage without blueprint and with args for view function:  
`url_for("hello", who="World")`  
Example usage with blueprint:  
`url_for("some_blueprint.hello")`  

#### Templates
