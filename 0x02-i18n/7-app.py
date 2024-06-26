#!/usr/bin/env python3
"""Appropriate timezones"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict
import pytz


class Config(object):
    """Class for babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Retrieves user based on user id"""
    user_id = request.args.get('login_as')

    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """Routines before request resolution"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Gets locale from URL"""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']

    from_header = request.headers.get('locale', '')
    if from_header in app.config["LANGUAGES"]:
        return from_header

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Gets timezone from a web page"""
    tz = request.args.get('timezone', '').strip()

    if not tz and g.user:
        tz = g.user['timezone']

    try:
        return pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Returns the index.html page"""
    return render_template('5-index.html')

# babel.init_app(app, locale_selector=get_locale)


if __name__ == "__main__":
    app.run(debug=True)
