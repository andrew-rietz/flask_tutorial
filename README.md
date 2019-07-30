# flask_tutorial
Full tutorial available in flask documentation:
https://flask.palletsprojects.com/en/1.1.x/tutorial/

For this tutorial I created an app called **our_flask_app**. The tutorial uses
a SQLite database for simplicity.

## Table of Contents
1. [Application Setup](#application-setup)
2. [Define and Access Database](#define-and-access-database)
3. [Blueprints and Views](#blueprints-and-views)
4. [Templates](#templates)
5. [Static Files](#static-files)
6. [A Second Blueprint](#a-second-blueprint)
7. [Make the Project Installable](#make-the-project-installable)


****
## Application Setup
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)  
The most straightforward way to create a Flask application is to
create a global Flask instance directly at the top of your code.
While this is simple and useful in some cases, but can cause some  
issues as the project grows.

Instead of creating a Flask instance globally, create it inside a
function. This function is known as the `application factory`. Any
configuration, registration, and other setup the application needs
will happen inside the function, then the application will be
returned.  
[See `application factory`](our_flask_app/__init__.py)  


> Test Application Works

```
export FLASK_APP=our_flask_app
export FLASK_ENV=development
flask run
```


****
## Define and Access Database
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


****
## Blueprints and Views
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


****
## Add views to the Blueprint
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
log the user in and store their data in the `session`. Data stored
in the `session` is available for future requests.  
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


****
## Templates
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/)  
Before your views can render on the server, we need to write the
`templates`. Our views are all calling `render_template()`, which,
currently causes an error because there are no templates.

`Templates` are files that contain static data as well as
placeholders for dynamic data. A template is rendered with specific
data to produce a final document. Flask uses the
[Jina](http://jinja.pocoo.org/docs/2.10/templates/)
template library to render templates.

We'll use templates to render HTML that will display in the
browser. In Flask, Jinja is configured to `autoescape` any data
that is rendered in HTML templates, so it's safe to render user
input. Any characters they've entered that could interfere with
the HTML (such as `<` and `>`) will be escaped with safe values
that look the same in the browser but don't cause unwanted effects.

In a template, anything between `{{` and `}}` is an expression
that will be output to the final document. `{%` and `%}`denote
a control flow statement (like `if` or `for`). Blocks are denoted
by start and end tags rather than indentation since static text
within a block could change indentation.

> The Base Layout

Each page in the application will have the same basic layout
around a different body. Instead of writing the entire HTML
structure in each template, each template will `extend` a base
template and override specific sections.

`g` is automatically available in templates and is a global
namespace for holding any data you want during a single app
context. An app context lasts for one request/response cycle.
`g` is not appropriate for storing data across requests. To
store data across requests you need to use a database, redis,
the session, or another external data source for persisting data.

Our template defines three blocks that will be overridden in the
other templates.  
- `{% block title %}` will change the title displayed in the
browser’s tab and window title.
- `{% block header %}` is similar to title but will change the
title displayed on the page.
- `{% block content %}` is where the content of each page goes,
such as the login form or a blog post

The base template is directly in the `templates` directory. To
help with organization, the templates for a blueprint should be
placed in a directory with the same name as the blueprint.  
[See `base.html`](our_flask_app/templates/base.html)

> Register

`{% extends 'base.html' %}` tells Jinja that this template should
replace the blocks from the base template. All the rendered content
must appear inside `{% block %}` tags that override blocks from the
base template.  
[See `register.html`](our_flask_app/templates/auth/register.html)

> Log In

Identical to register, except for a couple labels
[See `login.html`](our_flask_app/templates/auth/login.html)


****
## Static Files
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/static/)

The authentication views and templates work, but they look very
plain right now. Some CSS can be added to add style to the HTML
layout you constructed. The style won’t change, so it’s a static
file rather than a template.

Flask automatically adds a static view that takes a path relative
to the `our_flask_app/static` directory and serves it. The
base.html template already has a link to the style.css file:  
`{{ url_for('static', filename='style.css') }}`  

Besides CSS, other types of static files might be files with
JavaScript functions, or a logo image. They are all placed under
the `our_flask_app/static` directory and referenced with
`url_for('static', filename='...')`.


****
## A Second Blueprint
You can create more than one `blueprint` for a given app. We'll
create a blog blueprint that should list all posts, allow logged
in users to create posts, and allow the author of a post to edit
or delete it.

As you implement each view, keep the development server running. As
you save your changes try going to the URL in your browser and
testing them out.

> The Blueprint

Define the blueprint and register it in the application factory.
Unlike the `auth` blueprint, the `blog` blueprint does not have a
`url_prefix`. So the `index` will be at `/`, the `create` view at
`/create` and so on. The blog is the main feature of our app, so
it makes sense that the blog index will be the main index.  

However, the endpoint for the index view (a view associate with the
blog blueprint) will be `blog.index`. Some of the authentication
views referred to a plain `index` endpoint. `app.add_url_rule()`
(in the application factory) associate the name `index` with the `/`
url so that `url_for("index")` or `url_for("blog.index")` will both
work, generating the same `/` URL either way.

In another application you might give the blog blueprint a
`url_prefix` and define a separate `index` view in the application
factory, similar to the `hello` view. Then the `index` and
`blog.index` endpoints and URLs would be different.

> Index

The index will show all of the posts, most recent first. a `JOIN`
is used so that the author information from the user table is
available in the result.

When a user is logged in, the header block adds a link to the
create view. When the user is the author of a post, they’ll see an
“Edit” link to the update view for that post. `loop.last` is a
special variable available inside Jinja for loops. It’s used to
display a line after each post except the last one, to visually
separate them.

> Create

The `create` view works the same as the auth register view. Either
the form is displayed or the posted data is validated and the post
is added to the database or an error is shown.

The `login_required` decorator we wrote earlier is used on the
blog views. A user must be logged in to visit these views, otherwise
they'll be redirected to the login page.

> Update

Both the `update` and `delete` views will need to fetch a `post` by
`id` and check if the author matches the logged in user. To avoid
duplicating code, you can write a function to get the `post` and
call if from each view.

Unlike the views you’ve written so far, the update function takes
an argument, id. That corresponds to the `<int:id>` in the route. A
real URL will look like `/1/update`. Flask will capture the 1,
ensure it’s an int, and pass it as the id argument. If you don’t
specify `int:` and instead do `<id>`, it will be a string.

The template has two forms. The first posts the edited data to the
current page (`/<id>/update`). The other form contains only a button
and specifies an `action` attribute that posts to the delete view
instead. The button uses some Javascript to show a confirmation
dialog before submitting.

The pattern `{{ request.form["title"] or post["title"] }}` is
used to choose what data appears in the form. When the form hasn't
been submitted, the original `post` data appears, but if invalid
form data were posted you would want to display that so the user
can fix the error, so `request.form` is used instead.

`request` is another variable that's automatically available in
templates. `request` is a global object that parses incoming
request data for you  and gives you access to it through that
global object.

> Delete

The delete view doesn’t have its own template, the delete button is
part of `update.html` and posts to the `/<id>/delete` URL. Since
there is no template, it will only handle the `POST` method and
then redirect to the `index` view.

****

Congratulations, you’ve now finished writing your application! Take some time to try out everything in the browser. However, there’s still more to do before the project is complete.

****


## Make the Project Installable
[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/install/)

Making your project installable means that you can build a
`distribution` file and install that in another environment just
like you installed Flask in your project's environment. This
makes deploying your project the same as installing any other
library, so you're using all the standard Python tools to
manage everything.

Installing also comes with other benefits that might not be obvious
from the tutorial or as a new Python user, including:
- Currently, Python and Flask understand how to use the package
we created only because you're running them from your project's
directory. Installing means you can import it no matter where you
run from.
- You can manage your project's dependencies just like other
packages do, so `pip install yourproject.whl` installs them
- Test tools can isolate your test environment from your
development environment.

**NOTE: This is being introduced late in the tutorial, but in
your future projects you should always start with this.**

> Describe the Project

The `setup.py` file describes your project and the files that
belong to it.

`packages` tells Python what package directories (and the Python
files they contain) to include. `find_packages` finds these
directories automatically so you don't have to type them out. To
include other files, such as the static and template directories,
`include_package_data` is set. Python needs another file named
`MANIFEST.in` to tell what this other data is.

The `MANIFEST` file tells Python to copy everything in the `static`
and `templates` directories, and the `schema.sql` file, but to
exclude all bytecode files.

> Install the Project

Use `pip` to install your project in the virtual environment.  
`$ pip install -e .`  
This tells pip to find `setup.py` in the current directory and
install it in `editable` or `development` mode. Editable mode means
that as you make changes to your local code, you'll only need to
re-install if you change the metadata about the project, such
as its dependencies.

You can observe that the project is now installed with `pip list`

After the steps above, nothing changes from how you've been running
your project so far. `FLASK_APP` is still set to `our_flask_app` and
`flask run` still runs the application, but you can call it from
anywhere, not just the `flask-tutorial` directory.
