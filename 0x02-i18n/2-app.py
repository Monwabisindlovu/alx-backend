#!/usr/bin/env python3
"""A babel and flask app"""

from flask import Flask, render_template, request
from flask_babel import Babel

class Config:
    """
    Setting the languages and the locale and timezone
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# Function to get locale from request
@babel.localeselector
def get_locale():
    """
    Get locale from request using request.accept_languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def hello_world():
    """to run on the website"""
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

