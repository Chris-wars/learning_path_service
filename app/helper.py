import requests, uuid
from typing import Any
from datetime import datetime


def gen_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def now_dt():
    return datetime.now()


def get_json(url: str, timeout: int = 10) -> Any:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]

    return data
