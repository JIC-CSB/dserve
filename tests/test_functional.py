"""Functional tests for dserve server."""

import os

import pytest
import requests
from flask import request

HERE = os.path.dirname(__file__)
SAMPLE_DATASET_PATH = os.path.join(HERE, "data", "cotyledon_images")

PORT=5000
TEST_SERVER = "http://127.0.0.1:{}".format(PORT)

def test_root():
    url = TEST_SERVER
    r = requests.get(url)
    assert r.status_code == 200
    assert r.headers['content-type'].find("json") != -1

    content = r.json()
    assert "uuid" in content

    expected_content = {
        "_links": {
           "self": { "href": "/"},
           "items": { "href": "/items" },
           "overlays": { "href": "/overlays" }
        },
        "uuid": "4396cc68-2ded-4ca6-9992-bd24c11f5e09",
        "dtool_version": "0.12.1",
        "name": "cotyledon_images",
        "creator_username": "olssont",
    }
    assert content == expected_content

