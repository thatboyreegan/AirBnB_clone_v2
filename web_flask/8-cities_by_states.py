#!/usr/bin/python3
""" This script that starts a Flask web application - 8-cities_by_states.py"""

from models.state import State
from models import storage
from flask import Flask, render_template, request


app = Flask(__name__)


@app.teardown_appcontext
def tearDownApp(self):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    objs = storage.all(State)
    obj_list = sorted(objs.values(), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=obj_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
