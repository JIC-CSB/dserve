"""Simple image server."""

import os
import json

from flask import Flask, send_file, jsonify

from dtool import DataSet

app = Flask(__name__)

DATA_ROOT = '/Users/hartleym/data_repo'


@app.route('/<project>/<dataset_name>')
def show_hashes(project, dataset_name):
    print(project, dataset_name)

    dataset_path = os.path.join(DATA_ROOT, dataset_name)

    dataset = DataSet.from_path(dataset_path)

    return jsonify(dataset.descriptive_metadata)


@app.route('/<project>/<dataset>/<file_hash>')
def hello_world(project, dataset, file_hash):

    dataset_path = os.path.join(DATA_ROOT, project, dataset)
    manifest_path = os.path.join(dataset_path, 'manifest.json')

    with open(manifest_path, 'r') as fh:
        manifest = json.load(fh)

    dtool_file = os.path.join(dataset_path, '.dtool-dataset')
    with open(dtool_file) as fh:
        dataset_info = json.load(fh)

    file_list = manifest['file_list']
    keyed_by_hash = {entry['hash']: entry for entry in file_list}

    manifest_root = dataset_info['manifest_root']

    data_root = os.path.join(dataset_path, manifest_root)

    path = keyed_by_hash[file_hash]['path']
    fq_data_path = os.path.join(data_root, path)
    data_mimetype = keyed_by_hash[file_hash]['mimetype']

    return send_file(fq_data_path, data_mimetype)
