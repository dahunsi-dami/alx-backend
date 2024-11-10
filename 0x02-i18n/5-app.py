#!/usr/bin/env python3
"""
Basic Flask app w/ mock user login & Babel localization.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _


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
    Picks best match w/ user's-
    -supported language defined in Config class.

    If locale parameter is in URL & matches a supported language,
    it is used. Otherwise, best match from request's accepted-
    -languages is returned.

    Returns:
        str: the best match language code.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Index route for Flask app that renders 0-index.html
    in templates dir.

    Returns:
        str: rendered HTML of 0-index.html.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    """
    Entry point to flask app.
    Checks if module is run directly, and only then
    does it run the app.
    """
    app.run(debug=True)
