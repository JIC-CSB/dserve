"""Functional tests for dserve server."""
import os

import requests

HERE = os.path.dirname(__file__)
SAMPLE_DATASET_PATH = os.path.join(HERE, "data", "cotyledon_images")

PORT = 5000
TEST_SERVER = "http://127.0.0.1:{}".format(PORT)


def test_root_route():
    url = TEST_SERVER
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

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


def test_items_route():
    url = "/".join([TEST_SERVER, "items"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

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


def test_overlays_route():
    url = "/".join([TEST_SERVER, "overlays"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

    expected_content = {
        "_links": {
            "self": {"href": "/overlays"},
            "coordinates": {"href": "/overlays/coordinates"}},
    }
    assert r.json() == expected_content


def test_specific_item_route():
    url = "/".join([
        TEST_SERVER,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

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


def test_specific_item_raw_route():
    url = "/".join([
        TEST_SERVER,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "raw"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("png") != -1
    assert int(r.headers['content-length']) == 276


def test_specific_item_overlay_route():
    url = "/".join([
        TEST_SERVER,
        "items",
        "290d3f1a902c452ce1c184ed793b1d6b83b59164",
        "coordinates"])
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

    expected_content = {"x": 4.0, "y": 5.6}
    assert r.json() == expected_content
