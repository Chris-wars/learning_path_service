import os, json
from typing import Dict, List, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYSTEM_PROMPT = """Sie sind ein einfacher Lehrplan-Planer.
Geben Sie STRENG JSON zurück mit:
- "summary": kurzer String
- "milestones": Array von 3-8 Meilensteinen mit:
  milestoneId, type ("skill"|"topic"), label, skillId (oder null), topicId (oder null),
  resources: [{resourceId, why}], status: "pending"
Verwenden Sie nur IDs, die in den bereitgestellten Katalogen existieren. Kein zusätzlicher Text.
"""

def ask_openai_for_plan(
    desired_skills: List[str],
    desired_topics: List[str],
    topics: List[Dict[str, Any]],
    skills: List[Dict[str, Any]],
    resources: List[Dict[str, Any]]) -> Dict[str, Any]:

    if not client:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    user_payload = {
        "desiredSkills": desired_skills,
        "desiredTopics": desired_topics,
        "topics": [{
            "id": topic.get("id"), 
            "name": topic.get("name")
            } for topic in topics],
        "skills": [{
            "id": skill.get("id"), 
            "name": skill.get("skill"), 
            "topicID": skill.get("topicID")
            } for skill in skills],
        "resources": [{
            "id": resource.get("id"),
            "title": resource.get("title"), 
            "description": resource.get("description", "")
        } for resource in resources]
    }

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
        ],
        temperature=OPENAI_TEMPERATURE,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
