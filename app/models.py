from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
from datetime import datetime

MilestoneType = Literal["skill", "topic"]
MilestoneStatus = Literal["pending", "in-progress", "done"]

class GenerateRequest(BaseModel):
    userId: Optional[str] = None
    desiredSkills: List[str] = Field(default_factory=list)
    desiredTopics: List[str] = Field(default_factory=list)

class ResourceRef(BaseModel):
    resourceId: str
    why: Optional[str] = None

class Milestone(BaseModel):
    milestoneId: str
    type: MilestoneType
    label: str
    skillId: Optional[str] = None
    topicId: Optional[str] = None
    resources: List[ResourceRef] = Field(default_factory=list)
    status: MilestoneStatus = "pending"

class LearningPath(BaseModel):
    pathId: str
    userId: Optional[str] = None
    goals: Dict[str, List[str]]
    summary: Optional[str] = None
    milestones: List[Milestone]
    createdAt: datetime
    updatedAt: datetime