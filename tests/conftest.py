import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):

    from app import db

    _store = {}

    def mock_save_path(lpath):
        _store[lpath["id"]] = lpath
        return lpath
    
    def mock_list_paths(user_id=None):
        values = list(_store.values())
        if user_id:
            values = [path for path in values if path.get("userId") == user_id]
        return values
    
    def mock_get_path_by_id(path_id):
        return _store.get(path_id)
    
    monkeypatch.setattr(db, "save_path", mock_save_path, raising=True)
    monkeypatch.setattr(db, "list_paths", mock_list_paths, raising=True)
    monkeypatch.setattr(db, "get_path_by_id", mock_get_path_by_id, raising=True)


    from app import clients

    def mock_fetch_topics():
        return [
            {"id": "t-react", "name": "React"},
            {"id": "t-testing", "name": "Testing"}
        ]
    
    def mock_fetch_resources():
        return [
            {"id": "r-1", "title": "Intro to Testing"},
            {"id": "r-2", "title": "React Basics"},
        ]
    