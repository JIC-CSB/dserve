"""Simple dataset server."""

import os
import json
import argparse

from flask import (
    Flask,
    send_file,
    jsonify,
    request,
    url_for
)

from flask_cors import CORS, cross_origin

from dtool import DataSet, NotDtoolObject

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DATA_ROOT = '/Users/hartleym/data_repo'


@app.route('/datasets')
def show_datasets():
    all_datasets = find_all_datasets(DATA_ROOT)

    dataset_names = list(all_datasets.keys())

    return jsonify(dataset_names)


@app.route('/dataset/<dataset_name>')
def show_dataset_metadata(dataset_name):

    dataset_path = os.path.join(DATA_ROOT, dataset_name)

    dataset = DataSet.from_path(dataset_path)

    return jsonify(dataset.descriptive_metadata)


@app.route('/dataset/<dataset_name>/hashes')
def show_dataset_hashes(dataset_name):

    dataset_path = os.path.join(DATA_ROOT, dataset_name)

    dataset = DataSet.from_path(dataset_path)

    file_list = dataset.manifest["file_list"]

    hashes = [item['hash'] for item in file_list]

    return jsonify(hashes)


@app.route('/dataset/<dataset_name>/item/<item_hash>')
def server_dataset_item(dataset_name, item_hash):

    dataset_path = os.path.join(DATA_ROOT, dataset_name)
    dataset = DataSet.from_path(dataset_path)
    # FIXME - BROKEN FUNCTION
    # item_path = dataset.item_path_from_hash(item_hash)

    items_by_hash = {item['hash']: item
                     for item in dataset.manifest["file_list"]}

    item_path = os.path.join(
        dataset._abs_path,
        dataset.data_directory,
        items_by_hash[item_hash]['path']
    )
    data_mimetype = items_by_hash[item_hash]['mimetype']

    return send_file(item_path, data_mimetype)


@app.route('/dataset/<dataset_name>/item/<item_hash>/coords')
def find_item_overlay(dataset_name, item_hash):

    dataset_path = os.path.join(DATA_ROOT, dataset_name)
    dataset = DataSet.from_path(dataset_path)

    coords = dataset.overlays["coords"][item_hash]

    print(coords)

    return jsonify(coords)


@app.route('/dataset/<dataset_name>/item/<item_hash>/update_coords',
           methods=['POST'])
def set_item_coords(dataset_name, item_hash):

    dataset_path = os.path.join(DATA_ROOT, dataset_name)
    dataset = DataSet.from_path(dataset_path)

    coords = dataset.overlays["coords"]

    new_coords_value = request.get_json()

    coords[item_hash] = new_coords_value

    dataset.persist_overlay("coords", coords)

    print(new_coords_value)

    return item_hash


def identifiers_where_overlay_is_true(dataset, overlay_name):

    overlays = dataset.overlays
    selected = [identifier
                for identifier in dataset.identifiers
                if overlays[overlay_name][identifier]]

    return selected


@app.route('/givemejpegurls', methods=['GET'])
@cross_origin()
def get_all_jpegs():

    dataset_name = 'cad_tilling_2016'
    dataset_path = os.path.join(DATA_ROOT, dataset_name)
    dataset = DataSet.from_path(dataset_path)

    jpeg_identifiers = identifiers_where_overlay_is_true(dataset, "is_jpeg")

    urls = [url_for("server_dataset_item",
                    dataset_name=dataset_name,
                    item_hash=identifier)
            for identifier in jpeg_identifiers]

    return jsonify(urls)


def find_all_datasets(path):
    """Return dictionary of datasets in given path, keyed by name of dataset.
    Names are expected to be unique.

    :param path: Path to directory containing datasets.
    :returns: Dictionary of datasets.
    """

    directories = [d
                   for d in os.listdir(path)
                   if os.path.isdir(os.path.join(path, d))]

    all_datasets = {}
    for d in directories:
        try:
            dataset = DataSet.from_path(os.path.join(path, d))
            all_datasets[dataset.name] = dataset
        except NotDtoolObject:
            pass

    return all_datasets


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('path', help='Path to data collectiont to server')

    args = parser.parse_args()

    print(find_all_datasets(args.path))


if __name__ == '__main__':
    app.run(debug=True)
