import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .db import mongo, paths, ping
from .clients import fetch_topics, fetch_skills, fetch_resources
from .llm import ask_openai_for_plan
from .models import GenerateRequest, LearningPath, Milestone
from .helpers import gen_id, now_dt

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="Learning Path Generator", version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"service": "learning-path-generator", "docs":"/docs", "health": "/healthz"}


@app.get("/healthz")
def healthz():
    try:
        ping()
    except Exception as e:
        raise HTTPException(500, f"Mongo database down: {e}")
    return {"status": "ok", "db": "up"}


@app.post("/generate", response_model=LearningPath)
def generate_path(body: GenerateRequest = Body(...)):
    try:
        topics = fetch_topics()
        skills = fetch_skills()
        resources = fetch_resources()
    except Exception as e:
        raise HTTPException(502, f"Upstream error: {e}")
    
    try:
        plan = ask_openai_for_plan(
            body.desiredSkills,
            body.desiredTopics,
            topics,
            skills,
            resources
            )
    except Exception as e:
        raise HTTPException(502, f"OpenAI error: {e}")
    
    milestones: List[Dict[str, Any]] = []
    for idx, milestone in enumerate(plan.get("milestones", []), start=1):
        milestones.append({
            "milestoneId": milestone.get("milestoneId") or f"m{idx}",
            "type": milestone.get("type"),
            "label": milestone.get("label"),
            "skillId": milestone.get("skillId"),
            "topicId": milestone.get("topicId"),
            "resources": milestone.get("resources", []),
            "status": milestone.get("status", "pending")
        })

    doc = {
        "pathId": gen_id("lp"),
        "userId": body.userId,
        "goals": {"skills": body.desiredSkills, "topics": body.desiredTopics},
        "summary": plan.get("summary", ""),
        "milestones": milestones,
        "createdAt": now_dt(),
        "updatedAt": now_dt()
    }

    paths.insert_one(doc)

    doc.pop("_id", None)
    return doc


@app.get("/paths", response_model=List[LearningPath])
def list_paths(userId: Optional[str] = Query(None)):
    query = {}
    
    if userId:
        query["userId"] = userId
    
    items = list(paths.find(query).sort("createdAt", -1))

    for item in items:
        item.pop("_id", None)

    return items


@app.get("/paths/{pathId}", response_model=LearningPath)
def get_path(pathId: str = Path(...)):
    item = paths.find_one({"pathId": pathId})

    if not item:
        raise HTTPException(404, "Not found")
    
    item.pop("_id", None)

    return item


