import re
from datetime import datetime
import types
import builtins
import pytest
from app import helper


def test_gen_id_has_prefix_and_uuid():
    value = helper.gen_id("lp")
    assert value.startswith("lp-")
    assert re.match(r"^lp-[0-9a-fA-F-]{36}$", value)


def test_gen_id_ids_unique():
    prefix = "lp"
    value1 = helper.gen_id(prefix)
    value2 = helper.gen_id(prefix)
    assert value1 != value2


def test_now_dt_returns_datetime():
    date = helper.now_dt()
    assert isinstance(date, datetime)


class _MockResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
    def json(self):
        return self._payload
    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception("HTTP error")
    

def test_get_json_returns_plain_payload(monkeypatch):
    def mock_get(url, timeout=10):
        return _MockResponse([{"id": "a"}, {"id": "b"}])
    
    monkeypatch.setattr(helper.requests, "get", mock_get)

    response = helper.get_json("http://example/api")
    assert response == [{"id": "a"}, {"id": "b"}]


def test_get_json_unwrap_data_array(monkeypatch):
    def mock_get(url, timeout=10):
        return _MockResponse({"data": [{"id": "a"}, {"id": "b"}]})
    
    monkeypatch.setattr(helper.requests, "get", mock_get)

    response = helper.get_json("http://example/api")
    assert response == [{"id": "a"}, {"id": "b"}]
    