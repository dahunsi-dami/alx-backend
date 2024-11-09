#!/usr/bin/env python3
"""
Basic Flask app w/ Babel localization support and
URL based locale selection.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


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
    return render_template('4-index.html')


if __name__ == '__main__':
    """
    Entry point to flask app.
    Checks if module is run directly, and only then
    does it run the app.
    """
    app.run(debug=True)
