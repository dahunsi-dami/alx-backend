#!/usr/bin/env python3
"""Basic Flask app."""
from flask import Flask, render_template
from flask_babel import Babel


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


@app.route('/')
def index():
    """
    Index route for Flask app that renders 1-index.html
    in templates dir.

    Returns:
        str: rendered HTML of 1-index.html.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
