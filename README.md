Fyyur
-----

## Overview

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

![image](https://user-images.githubusercontent.com/74383191/183261966-cb671621-f439-4c7e-b28a-3a5e1cc2df39.png)
<figcaption>Test</figcaption>

The project involved building out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

Requirements for the functionality of the application were as follows. Users must be able to:

* create new venues, artists, and book new shows
* search for venues and artists
* learn more about a specific artist or venue

Fyyur was created as the final project for the SQL and Data Modeling for the Web module of [Udacity's Full Stack Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).

## Basic Structure
* The data models are located in `models.py`, which correspond to the database table schema.
* Controllers are located in `app.py`, and divided into artist, venue and show sections.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating new artists, venues and shows are located in `forms.py`

## Getting Started

### Installing Dependencies

Key dependencies and libraries include:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** as the ORM library of choice
 * **PostgreSQL** as the database of choice
 * **Python3** and **Flask** as the server language and server framework, resepctively
 * **Flask-Migrate** for creating and running schema migrations

1. Developers are expected to have Python3 and pip installed
2. Create a new virtual environment `python3 -m venv venv` and activate: `source venv/bin/activate`
3. Install all dependencies: `pip install -r requirements.txt`
4. Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Initialise the tables using the models defined within the flask application by running:

```bash
flask db upgrade
```

Populate the database using the `dummy_data.sql` script. From the home directory, run:

```
psql -d fyyur -a -f dummy_data.sql
```

### Running the Server

To start the application, run the following:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

With the server running, to access the application go to: [http://localhost:5000](http://localhost:5000)


## Guide

