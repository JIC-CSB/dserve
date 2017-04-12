"""Script for running the dserve server."""

import json

from flask import (
    Flask,
    jsonify,
)

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify("")

if __name__ == '__main__':
    app.run(debug=True)
