#!/usr/bin/env python3
"""Basic Flask app."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """
    Index route for Flask app that renders 0-index.html
    in templates dir.

    Returns:
        str: rendered HTML of 0-index.html.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
