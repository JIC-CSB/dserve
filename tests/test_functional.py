"""Functional tests for dserve server."""

import requests

TEST_SERVER = "http://127.0.0.1:5000"

def test_root():
    url = TEST_SERVER
    r = requests.get(url)
    assert r.status_code == 200
