#!/usr/bin/env python3
"""A babel and flask app"""

from flask import Flask, render_template, g, request
from flask_babel import Babel, _
import pytz

app = Flask(__name__)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Function to get user information based on user ID
def get_user(user_id):
    return users.get(user_id)

# Function to set user as global on flask.g
@app.before_request
def before_request():
    user_id = request.args.get('login_as')
    if user_id:
        g.user = get_user(int(user_id))
    else:
        g.user = None

# Babel initialization
babel = Babel(app)

# Function to get locale from user
@babel.localeselector
def get_locale():
    if g.user and 'locale' in g.user:
        return g.user['locale']
    else:
        return request.accept_languages.best_match(['en', 'fr'])

@app.route('/')
def hello_world():
    if g.user:
        return render_template('5-index.html', message=_("You are logged in as %(username)s.", username=g.user['name']))
    else:
        return render_template('5-index.html', message=_("You are not logged in."))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

