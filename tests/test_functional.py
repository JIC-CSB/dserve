"""Functional tests for dserve server."""

import os
import subprocess
import shutil
import time
import tempfile

import pytest
import requests

HERE = os.path.dirname(__file__)
APP = os.path.join(HERE, "..", "dserve", "__init__.py")
SAMPLE_DATASET_PATH = os.path.join(HERE, "data", "cotyledon_images")

TEST_SERVER = "http://127.0.0.1:{}"


@pytest.fixture(scope="module")
def run_server(request):
    port = "5001"
    server = subprocess.Popen(["python", APP, SAMPLE_DATASET_PATH, "-p", port])
    time.sleep(1)

    @request.addfinalizer
    def teardown():
        server.terminate()
    return TEST_SERVER.format(port)


@pytest.fixture()
def run_write_server(request):
    d = tempfile.mkdtemp()
    tmp_dataset_path = os.path.join(d, "cotyledon_images")
    shutil.copytree(SAMPLE_DATASET_PATH, tmp_dataset_path)

    port = "5002"
    server = subprocess.Popen(["python", APP, tmp_dataset_path, "-p", port])
    time.sleep(1)

    @request.addfinalizer
    def teardown():
        server.terminate()
        shutil.rmtree(d)

    return TEST_SERVER.format(port)


def test_root_route(run_server):
    url = run_server
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {
        "_links": {
            "self": {"href": "/"},
            "items": {"href": "/items"},
            "overlays": {"href": "/overlays"}
        },
        "uuid": "4396cc68-2ded-4ca6-9992-bd24c11f5e09",
        "dtool_version": "0.12.1",
        "name": "cotyledon_images",
        "creator_username": "olssont",
    }
    assert r.json() == expected_content


def test_items_route(run_server):
    url = "/".join([run_server, "items"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {
        "_links": {
            "self": {"href": "/items"},
        },
        "_embedded": {
            "items": [{
                "_links": {"self": {"href": "/items/290d3f1a902c452ce1c184ed793b1d6b83b59164"}},  # NOQA
                "identifier": "290d3f1a902c452ce1c184ed793b1d6b83b59164",
                "coordinates": {"x": 4.0, "y": 5.6},
                "mimetype": "image/png",
                "size": 276
            }, {
                "_links": {"self": {"href": "/items/09648d19e11f0b20e5473594fc278afbede3c9a4"}},  # NOQA
                "identifier": "09648d19e11f0b20e5473594fc278afbede3c9a4",
                "coordinates": {"x": 80.8, "y": 3.3},
                "mimetype": "image/png",
                "size": 276
            }],
            "number_of_items": 2,
            "total_size": 552
        }
    }
    assert r.json() == expected_content


def test_overlays_route(run_server):
    url = "/".join([run_server, "overlays"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {
        "_links": {
            "self": {"href": "/overlays"},
            "coordinates": {"href": "/overlays/coordinates"}},
    }
    assert r.json() == expected_content


def test_specific_item_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {
        "_links": {
            "self": {"href": "/items/290d3f1a902c452ce1c184ed793b1d6b83b59164"},  # NOQA
            "content": {"href": "/items/290d3f1a902c452ce1c184ed793b1d6b83b59164/raw"},  # NOQA
            "coordinates": {"href": "/items/290d3f1a902c452ce1c184ed793b1d6b83b59164/coordinates"}  # NOQA
        },
        "coordinates": {"x": 4.0, "y": 5.6},
        "mimetype": "image/png",
        "size": 276
    }
    assert r.json() == expected_content


def test_nonexisitng_specific_item_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "nonsense"])
    r = requests.get(url)
    assert r.status_code == 404


def test_specific_item_raw_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "raw"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("png") != -1
    assert r.headers['access-control-allow-origin'] == "*"
    assert int(r.headers['content-length']) == 276


def test_nonexisting_specific_item_raw_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "nonsense",
        "raw"])
    r = requests.get(url)
    assert r.status_code == 404


def test_specific_item_overlay_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "coordinates"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {"x": 4.0, "y": 5.6}
    assert r.json() == expected_content


def test_nonexisting_specific_item_overlay_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "nonsense",
        "coordinates"])
    r = requests.get(url)
    assert r.status_code == 404


def test_specific_item_nonexisting_overlay_route(run_server):
    url = "/".join([
        run_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "nonsense"])
    r = requests.get(url)
    assert r.status_code == 404


def test_specific_overlay_route(run_server):
    url = "/".join([run_server, "overlays", "coordinates"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {
        "290d3f1a902c452ce1c184ed793b1d6b83b59164": {"x": 4.0, "y": 5.6},
        "09648d19e11f0b20e5473594fc278afbede3c9a4": {"x": 80.8, "y": 3.3}
    }
    assert r.json() == expected_content


def test_nonexisting_specific_overlay_route(run_server):
    url = "/".join([run_server, "overlays", "nonsese"])
    r = requests.get(url)
    assert r.status_code == 404


def test_create_new_overlay(run_write_server):
    url = "/".join([run_write_server, "overlays", "results"])
    r = requests.put(url)
    assert r.status_code == 201

    r = requests.get(url)
    assert r.status_code == 200

    expected_content = {
        "290d3f1a902c452ce1c184ed793b1d6b83b59164": {},
        "09648d19e11f0b20e5473594fc278afbede3c9a4": {}
    }
    assert r.json() == expected_content


def test_create_new_overlay_does_not_overwrite(run_write_server):
    url = "/".join([run_write_server, "overlays", "results"])
    r = requests.put(url)
    assert r.status_code == 201
    r = requests.put(url)
    assert r.status_code == 409


def test_update_specific_item_in_overlay(run_write_server):
    url = "/".join([
        run_write_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "coordinates"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1
    assert r.headers['access-control-allow-origin'] == "*"

    expected_content = {"x": 4.0, "y": 5.6}
    assert r.json() == expected_content

    # application/json content-type not specified.
    r = requests.put(url, data={"x": 10.0, "y": -7.0})
    assert r.status_code == 422

    # application/json content-type specified, but data is not json.
    r = requests.put(
        url,
        data={"x": 10.0, "y": -7.0},
        headers={'content-type': 'application/json'})
    assert r.status_code == 400

    r = requests.put(
        url,
        data='{"x": 10.0, "y": -7.0}',
        headers={'content-type': 'application/json'})
    assert r.status_code == 201

    r = requests.get(url)
    expected_content = {"x": 10.0, "y": -7.0}
    assert r.json() == expected_content


def test_update_specific_item_in_nonexisting_overlay_404(run_write_server):
    url = "/".join([
        run_write_server,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "nonexisting"])

    r = requests.put(
        url,
        data='{"x": 10.0, "y": -7.0}',
        headers={'content-type': 'application/json'})
    assert r.status_code == 404


def test_update_specific_nonsese_item_in_overlay_404(run_write_server):
    url = "/".join([
        run_write_server,
        "items",
        "nonsense",
        "coordinates"])

    r = requests.put(
        url,
        data='{"x": 10.0, "y": -7.0}',
        headers={'content-type': 'application/json'})
    assert r.status_code == 404
