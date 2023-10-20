#!/usr/bin/python3
"""A module that displays a simple message using flask."""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display():
    """A method that displays hello HBNB!."""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)