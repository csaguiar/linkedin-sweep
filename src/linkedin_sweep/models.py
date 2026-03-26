from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Literal
import uuid

ActionType = Literal["like", "comment", "repost", "reply", "ignore"]
DecisionType = Literal["pending", "approved", "rejected", "done"]
SourceType = Literal["demo", "linkedin"]


@dataclass
class CandidateItem:
    author: str
    text: str
    url: str
    suggested_action: ActionType
    reason: str
    score: float
    source: SourceType = "demo"
    draft_comment: str | None = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: DecisionType = "pending"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CandidateItem":
        return cls(**data)
