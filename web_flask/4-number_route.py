#!/usr/bin/python3
"""A module that displays a simple message using flask."""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def display():
    """A method that displays hello HBNB!."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hello():
    """A function that returns a simple message."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def custom_route(text):
    """A custom route that displays a text."""
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def Cool_python(text='is cool'):
    """A route with a default value."""
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>')
def is_number(n):
    """Check if n is a number."""
    return f"{n} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)