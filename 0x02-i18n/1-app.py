#!/usr/bin/env python3
"""
Module for starting a basic Flask web application.
"""

from flask import Flask, render_template
from flask_babel import Babel

# Create Flask app instance
app = Flask(__name__)

# Instantiate the Babel object and store it in a module-level variable named babel
babel = Babel(app)

# Config class to set available languages and default locale/timezone for the app
class Config:
    """
    Config class to set available languages and default locale/timezone for the app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

# Use Config class as config for the Flask app
app.config.from_object(Config)

# Route to render the index.html template
@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('1-index.html', title="Welcome to Holberton", header="Hello world")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

