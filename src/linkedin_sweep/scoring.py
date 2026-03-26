from __future__ import annotations

from linkedin_sweep.models import CandidateItem


HIGH_SIGNAL_TERMS = [
    "ml", "machine learning", "deep learning", "llm", "ai", "toronto", "canada",
    "research", "production", "inference", "retrieval", "startup", "hiring",
]
LOW_SIGNAL_TERMS = [
    "comment ai", "top 100 prompts", "changed my life", "guru", "viral", "crushing it"]


def suggest_action(text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in LOW_SIGNAL_TERMS):
        return "ignore"
    if "congrats" in lower or "excited to start" in lower or "new role" in lower:
        return "reply"
    if any(term in lower for term in ["benchmark", "research", "production", "llm", "deep learning"]):
        return "comment"
    if any(term in lower for term in ["meetup", "event", "hiring", "launch"]):
        return "like"
    return "like"


def score_text(text: str) -> float:
    lower = text.lower()
    score = 0.3
    score += 0.12 * sum(term in lower for term in HIGH_SIGNAL_TERMS)
    score -= 0.2 * sum(term in lower for term in LOW_SIGNAL_TERMS)
    return max(0.0, min(0.99, round(score, 2)))


def reason_for(text: str, action: str) -> str:
    if action == "comment":
        return "Technical overlap; worthwhile to add a real point of view."
    if action == "reply":
        return "Looks like a direct interpersonal interaction worth acknowledging."
    if action == "like":
        return "Relevant enough for lightweight engagement."
    return "Low-signal or not strategically useful right now."


def draft_for(text: str, action: str) -> str | None:
    if action == "comment":
        return "Interesting angle. The production reality is usually where the tradeoffs become obvious — especially around latency, quality, and operational complexity."
    if action == "reply":
        return "Nice one — congrats. Wishing you a strong start." 
    return None


def enrich_item(item: CandidateItem) -> CandidateItem:
    action = suggest_action(item.text)
    item.suggested_action = action  # type: ignore[assignment]
    item.score = score_text(item.text)
    item.reason = reason_for(item.text, action)
    if not item.draft_comment:
        item.draft_comment = draft_for(item.text, action)
    return item
