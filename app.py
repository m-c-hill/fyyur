import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from pkg_resources import require
from forms import ShowForm, ArtistForm, VenueForm
from sqlalchemy import func
from datetime import datetime

# ====================
#  App Config
# ====================


app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
from models import Artist, Venue, Show

db.create_all()
migrate = Migrate(app, db)


# ====================
#  Filters
# ====================


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime


# ====================
#  Controllers
# ====================


@app.route("/")
def index():
    return render_template("pages/home.html")


# ====================
#  Venues
# ====================


@app.route("/venues")
def venues():
    data = []
    all_cities = Venue.query.with_entities(
        func.count(Venue.id), Venue.city, Venue.state
    ).group_by(Venue.city, Venue.state)

    for city in all_cities:
        current_city = city[1]
        current_state = city[2]
        venues_in_city = (
            Venue.query.filter_by(state=current_state)
            .filter_by(city=current_city)
            .all()
        )

        venues = []
        for venue in venues_in_city:
            num_upcoming_shows = len(
                Show.query.filter_by(venue_id=venue.id)
                .filter(Show.start_time > datetime.utcnow())
                .all()
            )

            venues.append(
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": num_upcoming_shows,
                }
            )

        data.append({"city": current_city, "state": current_state, "venues": venues})

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):

    venue = Venue.query.filter_by(id=venue_id).one()

    all_shows = Show.query.filter_by(venue_id=venue_id)

    past_shows_query = all_shows.filter(Show.start_time < datetime.utcnow()).all()
    past_shows = []
    for show in past_shows_query:
        artist = Artist.query.filter_by(id=show.artist_id).one()
        past_shows.append(
            {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    upcoming_shows_query = all_shows.filter(Show.start_time >= datetime.utcnow()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        artist = Artist.query.filter_by(id=show.artist_id).one()
        upcoming_shows.append(
            {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time,
            }
        )

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_show": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_venue.html", venue=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():

    search_term = request.form.get("search_term", "")
    search_results = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()

    venues = []
    for venue in search_results:
        num_upcoming_shows = len(
            Show.query.filter_by(venue_id=venue.id)
            .filter(Show.start_time < datetime.utcnow())
            .all()
        )
        venues.append(
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )

    response = {"count": len(search_results), "data": venues}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=search_term,
    )


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    error_occured = False

    try:
        venue = Venue(**request.form)
        db.session.add(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error_occured = True
    finally:
        db.session.close()

    if not error_occured:
        flash(
            f"An error occurred. Venue {request.form['name']} could not be listed.",
            category="error",
        )
    else:
        flash(f"Venue {request.form['name']} was successfully listed!", category="info")

    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


# ====================
#  Artists
# ====================


@app.route("/artists")
def artists():
    data = Artist.query.all()
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):

    artist = Artist.query.filter_by(id=artist_id).one()

    all_shows = Show.query.filter_by(artist_id=artist_id)

    past_shows_query = all_shows.filter(Show.start_time < datetime.utcnow()).all()
    past_shows = []
    for show in past_shows_query:
        venue = Venue.query.filter_by(id=show.venue_id).one()
        past_shows.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time,
            }
        )

    upcoming_shows_query = all_shows.filter(Show.start_time >= datetime.utcnow()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        venue = Venue.query.filter_by(id=show.venue_id).one()
        upcoming_shows.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time,
            }
        )

    artist_data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_artist.html", artist=artist_data)


@app.route("/artists/search", methods=["POST"])
def search_artists():

    search_term = request.form.get("search_term", "")
    search_results = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()

    artists = []
    for artist in search_results:
        num_upcoming_shows = len(
            Show.query.filter_by(artist_id=artist.id)
            .filter(Show.start_time < datetime.utcnow())
            .all()
        )
        artists.append(
            {
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )

    response = {"count": len(search_results), "data": artists}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=search_term,
    )


@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():

    error_occured = False

    try:
        artist = Artist(**request.form)
        db.session.add(artist)
        db.session.commit()
    except:
        db.session.rollback()
        error_occured = True
    finally:
        db.session.close()

    if not error_occured:
        flash(
            f"Artist {request.form['name']} was successfully listed!", category="info"
        )
    else:
        flash(
            f"An error occurred. Artist {request.form['name']} could not be listed.",
            category="error",
        )

    return render_template("pages/home.html")


# ====================
#  Shows
# ====================


@app.route("/shows")
def shows():

    shows = Show.query.all()

    data = []
    for show in shows:
        venue = Venue.query.filter_by(id=show.venue_id).one()
        artist = Artist.query.filter_by(id=show.artist_id).one()
        data.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():

    error_occured = False

    try:
        show = Show(**request.form)
        db.session.add(show)
        db.session.commit()
    except:
        db.session.rollback()
        error_occured = True
    finally:
        db.session.close()

    if not error_occured:
        flash(f"Show was successfully listed!", category="info")
    else:
        flash(f"An error occurred. Show could not be listed.", category="error")

    return render_template("pages/home.html")


# ============================
#  Error Handling and Logging
# ============================


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")


if __name__ == "__main__":
    app.run()
