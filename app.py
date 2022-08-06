import logging
from datetime import datetime, timedelta
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from forms import ArtistForm, ShowForm, VenueForm


# ====================
#  App Config
# ====================


app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
from models import Artist, Show, Venue

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
#  Controllers: Home
# ====================


@app.route("/")
def index():
    """
    Home page for Fyyur application, displaying recent listings
    """
    # Retrieve recently listed artists, venues and shows
    recent_artists = _retrieve_recent_artists()
    recent_venues = _retrieve_recent_venues()
    recent_shows = _retrieve_recent_shows()

    return render_template(
        "pages/home.html",
        artists=recent_artists,
        venues=recent_venues,
        shows=recent_shows,
    )


# =====================
#  Controllers: Venues
# =====================


@app.route("/venues")
def venues():
    """
    Retrieve information for all listed venues, grouped by city and render the venues page.
    """
    all_cities = Venue.query.with_entities(
        func.count(Venue.id), Venue.city, Venue.state
    ).group_by(Venue.city, Venue.state)

    # Retrieve and group the venues in each selected city
    data = []
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
    """
    Retrieve all shows for a given venue, past and present, and their associated artist
    information.
    """
    venue = Venue.query.filter_by(id=venue_id).one()
    all_shows = Show.query.filter_by(venue_id=venue_id)

    # Retrieve all past show information for the selected venue
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

    # Retrieve all upcoming show information for the selected venue
    upcoming_shows_query = all_shows.filter(Show.start_time >= datetime.utcnow()).all()
    upcoming_shows = []
    for show in upcoming_shows_query:
        artist = Artist.query.filter_by(id=show.artist_id).one()
        upcoming_shows.append(
            {
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
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
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_venue.html", venue=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    """
    Search for venues with names that match a given search term provided by the
    request body
    """
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
    """
    Render the venue submission form to allow users to submit new venues to the application
    """
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    """
    Create a new venue with details provided by post request body.
    """
    try:
        venue = Venue(**request.form)

        if not isinstance(venue.genres, list):
            venue.genres = [venue.genres]

        db.session.add(venue)
        db.session.commit()
        flash(f"Venue {request.form['name']} was successfully listed!", category="info")
    except:
        db.session.rollback()
        flash(
            f"An error occurred. Venue {request.form['name']} could not be listed.",
            category="error",
        )
    finally:
        db.session.close()

    return render_template("pages/home.html")


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    """
    Render the venue edit for a particular venue id
    """
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    if venue:
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.image_link.data = venue.image_link
        form.genres.data = venue.genres
        form.facebook_link.data = venue.facebook_link
        form.website_link.data = venue.website_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description

    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    """
    Update venue details based on the provided information in the post request body
    """
    venue = Venue.query.get(venue_id)
    try:
        venue.name = request.form.get("name")
        venue.city = request.form.get("city")
        venue.state = request.form.get("state")
        venue.address = request.form.get("address")
        venue.phone = request.form.get("phone")
        venue.image_link = request.form.get("image_link")
        venue.genres = request.form.get("genres")
        if not isinstance(venue.genres, list):
            venue.genres = [venue.genres]
        venue.facebook_link = request.form.get("website_link")
        venue.website_link = request.form.get("website_link")
        venue.seeking_talent = True if request.form.get("seeking_talent") else False
        venue.seeking_description = request.form.get("seeking_description")
        db.session.commit()
        flash(
            f"Artist {request.form['name']} was successfully updated!", category="info"
        )
    except:
        db.session.rollback()
        flash(
            f"An error occurred. Artist {request.form['name']} could not be updated.",
            category="error",
        )
    finally:
        db.session.close()

    return redirect(url_for("show_venue", venue_id=venue_id))


@app.route("/venues/<venue_id>", methods=["POST", "DELETE"])
def delete_venue(venue_id):
    """
    Delete a specific venue given a venue id and then render the remaining venues on the
    venues page
    """
    try:
        # To delete a venue, all shows associated with the venue also need to be deleted
        shows = Show.query.filter_by(venue_id=venue_id).all()
        show_count = 0
        for show in shows:
            show_count += 1
            db.session.delete(show)

        # Now all shows have deleted, proceed with deleting the venue
        venue = Venue.query.filter_by(id=venue_id).first()
        db.session.delete(venue)
        db.session.commit()
        flash(
            f"Venue '{venue.name}' has been deleted. {show_count} associated shows were also deleted.",
            category="info",
        )
    except:
        db.session.rollback()
        flash(
            f"An error occured: Venue could not be deleted.",
            category="info",
        )
    finally:
        db.session.close()

    return redirect(url_for("venues"))


# ====================
#  Artists
# ====================


@app.route("/artists")
def artists():
    """
    Retrieve information for all listed artists and render them alphabetically on the
    artists page.
    """
    data = Artist.query.order_by(Artist.name).all()
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    """
    Retrieve all shows for a given artist, past and present, and their associated venue
    information.
    """
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
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
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
                "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S"),
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
    """
    Search for artists with names that match a given search term provided by the
    request body
    """
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


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    """
    Render the artist submission form to allow users to submit new artists to the
    application.
    """
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    """
    Create a new artist with details provided by post request body
    """
    try:
        artist = Artist(**request.form)

        if not isinstance(artist.genres, list):
            artist.genres = [artist.genres]

        db.session.add(artist)
        db.session.commit()
        flash(
            f"Artist {request.form['name']} was successfully listed!", category="info"
        )

    except:
        db.session.rollback()
        flash(
            f"An error occurred. Artist {request.form['name']} could not be listed.",
            category="error",
        )
    finally:
        db.session.close()

    return render_template("pages/home.html")


@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    """
    Render the artist edit form for a particular venue id
    """
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    if artist:
        form.name.data = artist.name
        form.genres.data = artist.genres
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.website_link.data = artist.website_link
        form.facebook_link.data = artist.facebook_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.image_link.data = artist.image_link

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    """
    Update artist details based on the provided information in the post request body
    """
    artist = Artist.query.get(artist_id)

    try:
        artist.name = request.form.get("name")
        artist.genres = request.form.get("genres")
        if not isinstance(artist.genres, list):
            artist.genres = [artist.genres]
        artist.city = request.form.get("city")
        artist.state = request.form.get("state")
        artist.phone = request.form.get("phone")
        artist.website_link = request.form.get("website_link")
        artist.facebook_link = request.form.get("website_link")
        artist.seeking_venue = True if request.form.get("seeking_venue") else False
        artist.seeking_description = request.form.get("seeking_description")
        artist.image_link = request.form.get("image_link")
        db.session.commit()
        flash(
            f"Artist {request.form['name']} was successfully updated!", category="info"
        )
    except:
        db.session.rollback()
        flash(
            f"An error occurred. Artist {request.form['name']} could not be updated.",
            category="error",
        )
    finally:
        db.session.close()

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/artists/<int:artist_id>", methods=["POST", "DELETE"])
def delete_artist(artist_id):
    """
    Delete a specific artist given an artist id and then render the remaining artists on the
    artist page
    """
    try:
        # To delete an artist, all shows associated with the artist also need to be deleted
        shows = Show.query.filter_by(artist_id=artist_id).all()
        show_count = 0
        for show in shows:
            show_count += 1
            db.session.delete(show)

        # Now all shows have deleted, proceed with deleting the artist
        artist = Artist.query.filter_by(id=artist_id).first()
        db.session.delete(artist)
        db.session.commit()
        flash(
            f"Artist '{artist.name}' has been deleted. {show_count} associated shows were also deleted.",
            category="info",
        )
    except:
        db.session.rollback()
        flash(
            f"An error occured: Artist could not be deleted.",
            category="info",
        )
    finally:
        db.session.close()

    return redirect(url_for("artists"))


# ====================
#  Shows
# ====================


@app.route("/shows")
def shows():
    """
    Retrieve information for all listed shows, rendered on the shows page in chronological order.
    """
    shows = Show.query.order_by(Show.start_time).all()

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
    """
    Render the create new show form.
    """
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    """
    Create a new show based on information provided by the post request body.
    """
    try:
        show = Show(**request.form)
        db.session.add(show)
        db.session.commit()
        flash(f"Show was successfully listed!", category="info")
    except:
        db.session.rollback()
        flash(f"An error occurred. Show could not be listed.", category="error")
    finally:
        db.session.close()

    return render_template("pages/home.html")


# ===================
#  Utility functions
# ===================


def _retrieve_recent_artists():
    """Retrieve newly listed artists in the last 30 days"""
    return Artist.query.filter(
        Artist.date_created >= datetime.now() - timedelta(30)
    ).all()


def _retrieve_recent_shows():
    """Retrieve newly listed shows in the last 30 days"""
    return Show.query.filter(
        Artist.date_created >= datetime.now() - timedelta(30)
    ).all()


def _retrieve_recent_venues():
    """Retrieve newly listed venues in the last 30 days"""
    return Artist.query.filter(
        Artist.date_created >= datetime.now() - timedelta(30)
    ).all()


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
