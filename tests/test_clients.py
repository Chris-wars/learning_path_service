def test_fetch_skills_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "s1", "name": "Skill 1"}]
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_skills()

    assert response == [{"id": "s1", "name": "Skill 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/skills")

def test_fetch_resources_id_and__id(monkeypatch):
    # Test: _id wird zu id kopiert, falls id fehlt
    dummy = [
        {"_id": "abc", "title": "R1"},
        {"id": "def", "title": "R2"}
    ]
    def mock_get_json(url):
        assert url.endswith("/resources")
        return [dict(x) for x in dummy]  # Kopie
    monkeypatch.setattr(clients, "get_json", mock_get_json)
    result = clients.fetch_resources()
    # _id wird zu id kopiert, falls id fehlt
    assert any(r["id"] == "abc" for r in result)
    assert any(r["id"] == "def" for r in result)
    assert all("id" in r for r in result)
import pytest

from app import clients


class _Capture:
    def __init__(self):
        self.calls = []


def test_fetch_topics_calls_expected_url(monkeypatch):
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topics()
    
    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    assert cap.calls[0].endswith("/topics")
