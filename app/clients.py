import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from .helper import get_json

load_dotenv()

TOPICS_API_BASE_URL = os.getenv("TOPICS_API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
RESOURCES_API_BASE_URL = os.getenv("RESOURCES_API_BASE_URL", "http://localhost:5002").rstrip("/")


def fetch_topics() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE_URL}/topics")


def fetch_skills() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE_URL}/skills")


def fetch_resources() -> List[Dict[str, Any]]:
    items = get_json(f"{RESOURCES_API_BASE_URL}/resources")

    for item in items:
        if "id" not in item and "_id" in item:
            item["id"] = str(item["_id"])
    
    return items
