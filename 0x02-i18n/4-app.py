#!/usr/bin/env python3
"""Parametrize templates"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Class for babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Gets locale from URL"""
    # queries = request.query_string.decode('utf-8').plit('&')
    # queryTab = dict(map(
    #     lambda x: (x if '=' in x else '{}='.format(x)).split('='),
    #     queries,
    # ))

    # if 'locale' in queryTab:
    #     if queryTab['locale'] in app.config['LANGUAGES']:
    #         return queryTab['locale']
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return "fr"

@app.route('/')
def index():
    """Returns the index.html page"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(debug=True)
