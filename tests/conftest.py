
import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):

    from app import db

    _temp_store = []

    class _SimpleFind(list):
        def sort(self, *args, **kwargs):
            return self
        
    class _MockPaths:
        def insert_one(self, doc):
            print("[DEBUG][insert_one] before:", doc)
            data = dict(doc)
            data.setdefault("_id", f"auto-{len(_temp_store) + 1}")
            # pathId immer setzen, falls nicht vorhanden
            if "pathId" not in data:
                data["pathId"] = f"lp-{len(_temp_store) + 1}"
                doc["pathId"] = data["pathId"]  # Original-Objekt synchronisieren
            print("[DEBUG][insert_one] after:", data)
            _temp_store.append(data)
            class Result: ...
            result = Result()
            result.inserted_id = data["_id"]
            return result
        
        def find(self, query=None):
            return _SimpleFind(_temp_store)
        
        def find_one(self, query):
            print("[DEBUG][find_one] query:", query)
            query = query or {}
            # Suche nach allen Keys im Query-Dict
            for item in _temp_store:
                print("[DEBUG][find_one] check item:", item)
                match = True
                for k, v in query.items():
                    if item.get(k) != v:
                        match = False
                        break
                if match:
                    print("[DEBUG][find_one] FOUND:", item)
                    return item
            return None
        

    monkeypatch.setattr(db, "paths", _MockPaths(), raising=True)
    monkeypatch.setattr(db, "ping", lambda: True, raising=True)





    from app import clients
    from app import helper

    def mock_fetch_topics():
        return [
            {"id": "t-react", "name": "React"},
            {"id": "t-testing", "name": "Testing"}
        ]

    def mock_fetch_skills():
        return [
            {"id": "s1", "name": "React", "topic_id": "t-react"},
            {"id": "s2", "name": "Testing", "topic_id": "t-testing"}
        ]

    def mock_fetch_resources():
        return [
            {"id": "r-1", "title": "Intro to Testing"},
            {"id": "r-2", "title": "React Basics"},
        ]

    def mock_get_json(url, timeout=10):
        if "/topics" in url:
            return mock_fetch_topics()
        if "/skills" in url:
            return mock_fetch_skills()
        if "/resources" in url:
            return mock_fetch_resources()
        return []

    monkeypatch.setattr(clients, "fetch_topics", mock_fetch_topics)
    monkeypatch.setattr(clients, "fetch_skills", mock_fetch_skills)
    monkeypatch.setattr(clients, "fetch_resources", mock_fetch_resources)
    monkeypatch.setattr(helper, "get_json", mock_get_json)


    from app import llm

    def mock_ask_openai_for_plan(desired_skills, desired_topics, topics, skills, resources):
        return {
            "summary": "Simple demo learning path",
            "milestones": [
                {
                    "milestoneId": "m1",
                    "type": "skill",
                    "label": "Fundamentals",
                    "skillId": "s-basics",
                    "topicId": None,
                    "resources": [{"resourceId": "r-1", "why": "Start here"}],
                    "status": "pending",
                },
                {
                    "milestoneId": "m2",
                    "type": "topic",
                    "label": "Practice React",
                    "skillId": None,
                    "topicId": "t-react",
                    "resources": [{"resourceId": "r-2", "why": "Apply concepts"}],
                    "status": "pending",
                },
            ],
        }
    
    monkeypatch.setattr(llm, "ask_openai_for_plan", mock_ask_openai_for_plan, raising=True)

    
    return TestClient(app)