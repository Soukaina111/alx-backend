#!/usr/bin/env python3
"""
A Basic flask application
"""

# Import the necessary types from the typing module
from typing import (
    Dict, Union
)

# Import the Flask class from the flask module
from flask import Flask
# Import the g and request objects from the flask module
from flask import g, request
# Import the render_template function from the flask module
from flask import render_template
# Import the Babel class from the flask_babel module
from flask_babel import Babel

# Define a configuration class for the application


class Config(object):
    """
    Application configuration class
    """
    # Define the supported languages
    LANGUAGES = ['en', 'fr']
    # Set the default locale and timezone
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

# Instantiate the Flask application object


app = Flask(__name__)
# Load the configuration from the Config class

app.config.from_object(Config)

# Wrap the Flask application with the Babel extension

babel = Babel(app)

# Define a function to select the locale based on the request object


@babel.localeselector
def get_locale() -> str:
    """
    Gets locale from request object
    """
    # Get the 'locale' query parameter from the request
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# Define a dictionary of users


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Define a function to get a user by their ID


def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details
    Args:
        id (str): user id
    Returns:
        (Dict): user dictionary if id is valid else None
    """
    return users.get(int(id), 0)

# Define a function to be executed before each request


@app.before_request
def before_request():
    """
    Adds valid user to the global session object `g`
    """
    setattr(g, 'user', get_user(request.args.get('login_as', 0)))

# Define a route for the root URL '/'


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    # Use the render_template function to render the '5-index.html' template
    return render_template('5-index.html')

# Check if the script is being run directly (not imported as a module)


if __name__ == '__main__':
    # Run the Flask application
    app.run()
