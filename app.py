from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = "91dc917d6aced05982d51c9828e6db20"

import routes

