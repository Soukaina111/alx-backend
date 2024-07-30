#!/usr/bin/env python3
"""
A Basic flask application
"""

# Import the Flask class from the flask module
from flask import Flask
# Import the render_template function from the flask module
from flask import render_template

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the root URL '/'


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    # Use the render_template function to render the '0-index.html' template
    return render_template('0-index.html')

# Check if the script is being run directly (not imported as a module)


if __name__ == '__main__':
    # Run the Flask application
    app.run()
