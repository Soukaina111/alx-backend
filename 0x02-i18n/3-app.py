#!/usr/bin/env python3
"""
A Basic flask application
"""

# Import the Flask class from the flask module
from flask import Flask
# Import the request object from the flask module
from flask import request
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
    return request.accept_languages.best_match(app.config['LANGUAGES'])

# Define a route for the root URL '/'
@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    # Use the render_template function to render the '3-index.html' template
    return render_template('3-index.html')

# Check if the script is being run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application
    app.run()
