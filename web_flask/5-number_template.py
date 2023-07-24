#!/usr/bin/python3
""" This script starts a Flask web application - 5-number_template.py"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    return "C %s" % str(text.replace("_", " "))


@app.route('/python/(<text>)', strict_slashes=False)
def python(text='is cool'):
    return "Python %s" % str(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def numCheck(n):
    return "%d is a number" % int(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def numberTemplate(n):
    return render_template("5-number.html", num=n)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
