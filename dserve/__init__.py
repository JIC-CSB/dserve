"""Script for running the dserve server."""

import argparse
import json

from flask import (
    Flask,
    jsonify,
)

from dtoolcore import DataSet

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify(app._dataset._admin_metadata)

def main(dataset, port, debug):
    app._dataset = dataset
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_path")
    args = parser.parse_args()
    dataset = DataSet.from_path(args.dataset_path)
    main(dataset, 5000, True)
