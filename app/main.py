import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from . import db
from . import clients
from . import llm
from .models import GenerateRequest, LearningPath, Milestone
from .helper import gen_id, now_dt

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


@app.get("/paths/{pathId}", response_model=LearningPath)
def get_path(pathId: str):
    print("[DEBUG][get_path] called with pathId:", pathId)
    item = db.paths.find_one({"pathId": pathId})
    if not item:
        raise HTTPException(404, "Not Found")
    item.pop("_id", None)
    return item

@app.get("/")
def root():
    return {"service": "learning-path-generator", "docs":"/docs", "health": "/healthz"}



@app.get("/healthz")
def healthz():
    try:
        db.ping()
    except Exception as e:
        raise HTTPException(500, f"Mongo database down: {e}")
    return {"status": "ok", "db": "up"}


@app.post("/generate", response_model=LearningPath)
def generate_path(body: GenerateRequest = Body(...)):
    try:
        topics = clients.fetch_topics()
        skills = clients.fetch_skills()
        resources = clients.fetch_resources()
    except Exception as e:
        raise HTTPException(502, f"Upstream error: {e}")

    try:
        plan = llm.ask_openai_for_plan(
            body.desiredSkills,
            body.desiredTopics,
            topics,
            skills,
            resources
        )
    except Exception as e:
        raise HTTPException(502, f"OpenAI error: {e}")


    milestones = plan.get("milestones", [])

    doc = {
        "pathId": gen_id("lp"),
        "userId": body.userId,
        "goals": {"skills": body.desiredSkills, "topics": body.desiredTopics},
        "summary": plan.get("summary", ""),
        "milestones": milestones,
        "createdAt": now_dt(),
        "updatedAt": now_dt()
    }

    db.paths.insert_one(doc)
    return doc
    doc.pop("_id", None)
    return doc


@app.get("/paths", response_model=List[LearningPath])
def list_paths(userId: Optional[str] = Query(None)):
    query = {}
    
    if userId:
        query["userId"] = userId
    
    items = list(db.paths.find(query).sort("createdAt", -1))

    for item in items:
        item.pop("_id", None)

    # Liste aller gespeicherten Lernpfade zurückgeben
    return items


