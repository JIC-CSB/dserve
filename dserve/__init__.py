"""Script for running the dserve server."""

import argparse

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
    overlays = app._dataset.overlays
    total_size = 0
    items = []
    for i in app._dataset.manifest["file_list"]:
        total_size += i["size"]
        item = {
            "_links": {"self": {"href": "/items/{}".format(i["hash"])}},
            "identifier": i["hash"],
            "mimetype": i["mimetype"],
            "size": i["size"]
        }
        for key, value in overlays.items():
            item[key] = value[i["hash"]]
        items.append(item)
    content = {
        "_links": {
            "self": {"href": "/items"},
        },
        "_embedded": {
            "items": items,
            "number_of_items": len(items),
            "total_size": total_size
        }
    }
    return jsonify(content)


def specific_item(identifier):
    item = app._dataset.item_from_hash(identifier)
    content = {
        "_links": {
            "self": {"href": "/items/{}".format(identifier)},
            "content": {"href": "/items/{}/raw".format(identifier)},
        },
        "mimetype": item["mimetype"],
        "size": item["size"]
    }

    overlays = app._dataset.overlays
    for overlay_name, overlay in overlays.items():
        olink = {"href": "/items/{}/{}".format(identifier, overlay_name)}
        content["_links"][overlay_name] = olink
        content[overlay_name] = overlay[identifier]

    return jsonify(content)


@app.route("/items")
@app.route("/items/<identifier>")
def items(identifier=None):
    if identifier is None:
        return items_root()
    else:
        return specific_item(identifier)


@app.route("/overlays")
def overalys():
    overlays = app._dataset.overlays
    content = {
        "_links": {
            "self": {"href": "/overlays"}},
    }
    for overlay_name in overlays.keys():
        value = {"href": "/overlays/{}".format(overlay_name)}
        content["_links"][overlay_name] = value
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
