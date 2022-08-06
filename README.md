# Fyyur
-----

## Overview

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

![image](https://user-images.githubusercontent.com/74383191/183261966-cb671621-f439-4c7e-b28a-3a5e1cc2df39.png)|
|:--:|
| *Fyyur homepage* |

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

Here are a few brief video demonstrations of the key features of the Fyyur app:

### View Artists, Venues and Shows
https://user-images.githubusercontent.com/74383191/183263403-14f2c131-8348-4ef0-8c1e-279917260793.mp4

| *Browse artists, venues and their upcoming shows.* |

### Update a Venue

https://user-images.githubusercontent.com/74383191/183263406-75aa2770-e8e5-482c-93c4-1ffd28f8b5b3.mp4

| *The Dueling Pianos Bar is now looking for new talent and needs to update their listing.* |

### Create a New Artist

https://user-images.githubusercontent.com/74383191/183263409-9dd39819-fa7c-4082-9e26-aad268511e12.mp4

| *List a new artist, Behemoth, looking to book shows.* |

### Book a Show

https://user-images.githubusercontent.com/74383191/183263413-ff46594d-f0ce-46bf-8855-09747c5ae630.mp4

| *Create a new show with the newly listed band.* |

### Delete an Old Venue

https://user-images.githubusercontent.com/74383191/183263417-ec28d698-b4c4-48e2-98d5-2a6f26e64037.mp4

| *The venue 'Park Square Live Music & Coffee' has closed down and needs to be removed from the site, including all associated shows.* |
