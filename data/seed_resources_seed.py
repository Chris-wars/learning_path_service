#!/usr/bin/env python3
"""
Seed the Resources API with randomized demo resources.

Env:
  RESOURCES_API_BASE_URL   default: http://127.0.0.1:5002
  COUNT_PER_THEME          default: 10
  SLEEP_BETWEEN_MS         default: 20 (ms)   tiny delay between requests
  START_DATE_ISO           default: 2023-01-01 (random dates start)
  DRY_RUN                  default: ""  (set to "1" to only print payloads)

Usage:
  python seed_resources_api.py
"""

import os
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List
import requests

# -----------------------------
# Config
# -----------------------------
RESOURCES_API_BASE = os.getenv("RESOURCES_API_BASE_URL", "http://127.0.0.1:5002").rstrip("/")
COUNT_PER_THEME = int(os.getenv("COUNT_PER_THEME", "10"))
SLEEP_BETWEEN_MS = int(os.getenv("SLEEP_BETWEEN_MS", "20"))
START_DATE_ISO = os.getenv("START_DATE_ISO", "2023-01-01")
DRY_RUN = os.getenv("DRY_RUN", "").strip() in {"1", "true", "yes", "on"}

# Endpoint (adjust if your router is different)
RESOURCES_ENDPOINT = f"{RESOURCES_API_BASE}/resources"

# -----------------------------
# Data templates (same as your JS script)
# -----------------------------
THEMES: List[Dict] = [
    # Web
    {"k": "HTML",              "tags": ["HTML Structure", "Semantic Tags", "Forms & Validation"]},
    {"k": "CSS",               "tags": ["Flexbox", "Grid Layout", "Selectors & Specificity"]},
    {"k": "JavaScript",        "tags": ["Promises", "Async/Await", "Modules", "DOM"]},
    {"k": "Responsive Design", "tags": ["Media Queries", "Fluid Layouts", "Mobile-first"]},
    {"k": "Accessibility",     "tags": ["ARIA", "Keyboard Navigation", "Contrast"]},

    # Python
    {"k": "Python Basics",     "tags": ["Control Flow", "Functions", "Error Handling"]},
    {"k": "OOP in Python",     "tags": ["Classes", "Inheritance", "Dataclasses"]},
    {"k": "FastAPI",           "tags": ["Routing", "Request Models", "Middleware"]},
    {"k": "Pydantic",          "tags": ["Type Hints", "Validation"]},

    # Data/SQL/DevOps/Cloud/AI
    {"k": "Pandas",            "tags": ["DataFrames", "Aggregation", "Merging"]},
    {"k": "SQL",               "tags": ["Joins", "Indexes", "Transactions"]},
    {"k": "Docker",            "tags": ["Dockerfile", "Images", "Volumes"]},
    {"k": "Kubernetes",        "tags": ["Pods", "Deployments", "Services"]},
    {"k": "Terraform",         "tags": ["State", "Modules", "Plan/Apply"]},
    {"k": "AWS",               "tags": ["IAM", "EC2", "S3"]},
    {"k": "Security",          "tags": ["OWASP", "Secure Coding", "IAM"]},
    {"k": "Testing",           "tags": ["Unit", "Integration", "E2E"]},
    {"k": "Machine Learning",  "tags": ["Supervised", "Evaluation", "Overfitting"]},
]

TYPES = ["Course", "Article", "Video", "Documentation", "Project", "Book", "Tutorial"]
AUTHORS = ["auth-alice", "auth-bob", "auth-carol", "auth-dan", "auth-eve", "auth-frank"]


# -----------------------------
# Helpers
# -----------------------------
def rand(arr: List[str]) -> str:
    return random.choice(arr)


def rand_date(start_iso: str = START_DATE_ISO) -> datetime:
    start_dt = datetime.fromisoformat(start_iso)
    now = datetime.utcnow()
    delta = now - start_dt
    return start_dt + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def iso(dt: datetime) -> str:
    # Send ISO 8601 with Z (common for APIs backed by JS/Mongoose)
    return dt.replace(microsecond=0).isoformat() + "Z"


def build_resource(theme_key: str, tag: str) -> Dict:
    rtype = rand(TYPES)
    author_id = rand(AUTHORS)
    title = f"{theme_key}: {tag} — {rtype}"
    description = (
        f"A {rtype.lower()} covering {theme_key} with focus on {tag}. "
        "Includes practical examples and best practices."
    )
    created_at = rand_date()
    updated_at = max(created_at, rand_date())
    return {
        "title": title,
        "type": rtype,
        "description": description,
        "authorId": author_id,
        "createdAt": iso(created_at),
        "updatedAt": iso(updated_at),
    }


def post_json(url: str, payload: Dict) -> Dict:
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


# -----------------------------
# Seeding
# -----------------------------
def seed_resources() -> None:
    print(f"Using Resources API at: {RESOURCES_API_BASE}")
    print(f"POST -> {RESOURCES_ENDPOINT}")

    total = 0
    for theme in THEMES:
        for _ in range(COUNT_PER_THEME):
            tag = rand(theme["tags"])
            payload = build_resource(theme["k"], tag)

            if DRY_RUN:
                print("[DRY RUN] Would POST:", payload)
            else:
                data = post_json(RESOURCES_ENDPOINT, payload)
                # Expecting API returns created resource JSON with an 'id' (mapped from Mongo _id)
                rid = data.get("id") or data.get("_id") or "<?>"
                print(f"Created resource: {rid} — {payload['title']}")

            total += 1
            if SLEEP_BETWEEN_MS > 0:
                time.sleep(SLEEP_BETWEEN_MS / 1000.0)

    print(f"Total resources created: {total}")


if __name__ == "__main__":
    # Uncomment for reproducible runs
    random.seed(42)
    seed_resources()
