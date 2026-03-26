from __future__ import annotations

from datetime import datetime
from pathlib import Path

from linkedin_sweep.models import CandidateItem
from linkedin_sweep.scoring import enrich_item
from linkedin_sweep.storage import load_items, save_items, save_status


def collect_demo_items() -> dict:
    items = load_items()
    save_items(items)
    status = {
        "mode": "demo",
        "last_run": datetime.utcnow().isoformat(),
        "last_result": f"Loaded {len(items)} demo items.",
    }
    save_status(status)
    return status


def collect_from_linkedin_session(profile_dir: str | None = None) -> dict:
    """Placeholder collector.

    Real LinkedIn collection should run on the user's local machine with a real browser
    profile/session. This stub records intent and keeps the app usable until selectors,
    auth flow, and safety constraints are implemented.
    """
    profile_hint = profile_dir or str(Path.home() / ".config/linkedin-sweep/chrome-profile")
    status = {
        "mode": "linkedin_stub",
        "last_run": datetime.utcnow().isoformat(),
        "last_result": (
            "Collector stub only. Configure a local Playwright flow that reuses a real browser "
            f"session/profile. Suggested profile path: {profile_hint}"
        ),
    }
    save_status(status)
    return status


def import_manual_items(rows: list[dict]) -> int:
    items = load_items()
    for row in rows:
        item = CandidateItem(
            author=row.get("author", "Unknown"),
            text=row.get("text", ""),
            url=row.get("url", ""),
            suggested_action="like",
            reason="Imported item pending enrichment.",
            score=0.0,
            source="linkedin" if row.get("source") == "linkedin" else "demo",
        )
        items.append(enrich_item(item))
    save_items(items)
    status = {
        "mode": "manual_import",
        "last_run": datetime.utcnow().isoformat(),
        "last_result": f"Imported {len(rows)} items.",
    }
    save_status(status)
    return len(rows)
