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
    content = {
        "_links": {
           "self": { "href": "/"},
           "items": { "href": "/items" },
           "overlays": { "href": "/overlays" }
        },
        "uuid": app._dataset._admin_metadata["uuid"],
        "dtool_version": app._dataset._admin_metadata["dtool_version"],
        "name": app._dataset._admin_metadata["name"],
        "creator_username": app._dataset._admin_metadata["creator_username"],
    }
    return jsonify(content)

def main(dataset, port, debug):
    app._dataset = dataset
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_path")
    args = parser.parse_args()
    dataset = DataSet.from_path(args.dataset_path)
    main(dataset, 5000, True)
