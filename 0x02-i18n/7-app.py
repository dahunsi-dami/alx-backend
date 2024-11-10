#!/usr/bin/env python3
"""
Basic Flask app w/ mock user login & Babel localization.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    config for Flask app.
    Sets available languages.
    Sets Babel's default locale, timezone.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    TIMEZONES = [
        "UTC",
        "Europe/Paris",
        "US/Central",
        "Europe/London",
        "Vulcan"
    ]


app = Flask(__name__)

# We need to apply config to flask app now, so:
app.config.from_object(Config)

# Next, we instantiate the Babel object-
# -for localization support.
babel: Babel = Babel(app)


def _(message: str) -> str:
    """
    Translates a message to the current locale.
    """
    return gettext(message)


def get_user():
    """
    Gets a user w/ login_as URL parameter.

    Returns:
        dict: the user dict if found, else None.
    """
    user_id = request.args.get('login_as', type=int)
    return users.get(user_id)


@app.before_request
def before_request():
    """
    Before request handler that sets logged-in user-
    -in the global 'g' context if present.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best locale based on a priority order:
    1. URL parameter `locale`.
    2. User's preferred locale (if logged in).
    3. Request header `Accept-Language`.
    4. Default locale.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


app.jinja_env.globals['get_locale'] = get_locale


@babel.timezoneselector
def get_timezone():
    """
    Determines the best timezone based on a priority order:
    1. URL parameter `timezone`.
    2. User's preferred timezone (if logged in).
    3. Default timezone (UTC).

    Returns:
        str: the best match timezone.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    if g.user and g.user.get('timezone'):
        user_timezone = g.user.get('timezone')
        try:
            pytz.timezone(user_timezone)
            return user_timezone
        except UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.context_processor
def inject_timezone():
    """Make `get_timezone` available in all Jinja2 templates."""
    return dict(get_timezone=get_timezone)


@app.route('/')
def index() -> str:
    """
    Index route for Flask app that renders 0-index.html
    in templates dir.

    Returns:
        str: rendered HTML of 0-index.html.
    """
    return render_template('7-index.html', user=g.user)


if __name__ == '__main__':
    """
    Entry point to flask app.
    Checks if module is run directly, and only then
    does it run the app.
    """
    app.run(debug=True)
