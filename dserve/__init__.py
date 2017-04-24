"""Script for running the dserve server."""

import os
import argparse

from flask import (
    Flask,
    jsonify,
    send_file,
    abort,
    request,
)
from flask_cors import CORS, cross_origin

from dtoolcore import DataSet

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
@cross_origin()
def root():
    content = {
        "_links": {
            "self": {"href": "/"},
            "items": {"href": "/items"},
            "overlays": {"href": "/overlays"}
        },
        "uuid": app._dataset._admin_metadata["uuid"],
        "dtool_version": app._dataset._admin_metadata["dtool_version"],
        "name": app._dataset._admin_metadata["name"],
        "creator_username": app._dataset._admin_metadata["creator_username"],
    }
    return jsonify(content)


def items_root():
    items = []
    for i in app._dataset.manifest["file_list"]:
        item = {
            "_links": {"self": {"href": "/items/{}".format(i["hash"])}},
            "identifier": i["hash"],
        }
        items.append(item)

    content = {
        "_links": {
            "self": {"href": "/items"},
        },
        "_embedded": {
            "items": items,
        }
    }
    return jsonify(content)


def specific_item(identifier):
    try:
        item = app._dataset.item_from_identifier(identifier)
    except KeyError:
        abort(404)
    content = {
        "_links": {
            "self": {"href": "/items/{}".format(identifier)},
            "content": {"href": "/items/{}/raw".format(identifier)},
            "overlays": {"href": "/items/{}/overlays".format(identifier)},
        },
    }

    overlays = app._dataset.access_overlays()
    for overlay_name, overlay in overlays.items():
        content[overlay_name] = overlay[identifier]

    return jsonify(content)


@app.route("/items")
@app.route("/items/<identifier>")
@cross_origin()
def items(identifier=None):
    if identifier is None:
        return items_root()
    else:
        return specific_item(identifier)


@app.route("/items/<identifier>/raw")
@cross_origin()
def raw_item(identifier):
    try:
        item = app._dataset.item_from_identifier(identifier)
    except KeyError:
        abort(404)
    item_path = os.path.join(
        dataset._abs_path,
        dataset.data_directory,
        item["path"]
    )
    return send_file(item_path, item["mimetype"])


@app.route("/items/<identifier>/overlays")
@cross_origin()
def item_overlays(identifier):
    try:
        item = app._dataset.item_from_identifier(identifier)
    except KeyError:
        abort(404)
    content = {
        "_links": {
            "self": {"href": "/items/{}/overlays".format(identifier)},
        },
    }
    overlays = app._dataset.access_overlays()
    for overlay_name in overlays.keys():
        href = "/overlays/{}/{}".format(overlay_name, identifier)
        content["_links"][overlay_name] = {"href": href}

    return jsonify(content)


@app.route("/overlays/<overlay>/<identifier>", methods=["GET", "PUT"])
@cross_origin()
def item_overlay_content(overlay, identifier):
    overlays = app._dataset.access_overlays()
    try:
        requested_overlay = overlays[overlay]
        requested_overlay[identifier]
    except KeyError:
        abort(404)

    if request.method == "PUT":
        if not request.is_json:
            abort(422)
        new_value = request.get_json()
        requested_overlay[identifier] = new_value
        try:
            app._dataset.persist_overlay(
                overlay, requested_overlay, overwrite=True)
        except KeyError:
            abort(405)
        return "", 201
    elif request.method == "GET":
        value = requested_overlay[identifier]
        return jsonify(value)


def overlay_root():
    overlays = app._dataset.access_overlays()
    content = {
        "_links": {
            "self": {"href": "/overlays"}},
    }
    for overlay_name in overlays.keys():
        value = {"href": "/overlays/{}".format(overlay_name)}
        content["_links"][overlay_name] = value
    return jsonify(content)


def specific_overlay(overlay_name):
    overlays = app._dataset.access_overlays()
    try:
        overlay = overlays[overlay_name]
    except KeyError:
        abort(404)
    return jsonify(overlay)


def creaate_new_overlay(overlay_name):
    empty_overlay = app._dataset.empty_overlay()
    try:
        app._dataset.persist_overlay(overlay_name, empty_overlay)
    except IOError:
        abort(409)
    return "", 201


@app.route("/overlays")
@app.route("/overlays/<overlay_name>", methods=["GET", "PUT"])
@cross_origin()
def overalys(overlay_name=None):
    if overlay_name is None:
        return overlay_root()
    else:
        if request.method == "PUT":
            return creaate_new_overlay(overlay_name)
        elif request.method == "GET":
            return specific_overlay(overlay_name)


def main(dataset, port, debug):
    app._dataset = dataset
    app.run(port=port, debug=debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_path")
    parser.add_argument("-p", "--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    dataset = DataSet.from_path(args.dataset_path)
    main(dataset, args.port, args.debug)
