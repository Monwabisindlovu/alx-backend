#!/usr/bin/env python3
"""A babel and flask app"""

from flask import Flask, render_template, g, request
from flask_babel import Babel, _, get_timezone
import pytz
from datetime import datetime

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

# Function to get time zone
@babel.timezoneselector
def get_timezone():
    # Check if time zone is specified in URL parameters
    tz_param = request.args.get('timezone')
    if tz_param:
        try:
            pytz.timezone(tz_param)
            return tz_param
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    # Check user's preferred time zone
    if g.user and 'timezone' in g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    # Default to UTC
    return 'UTC'

# Function to get current time
def get_current_time():
    timezone = pytz.timezone(get_timezone())
    current_time = datetime.now(timezone)
    return current_time.strftime("%b %d, %Y, %I:%M:%S %p")

@app.route('/')
def hello_world():
    if g.user:
        return render_template('index.html', message=_("The current time is %(current_time)s.", current_time=get_current_time()))
    else:
        return render_template('index.html', message=_("You are not logged in."))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)

