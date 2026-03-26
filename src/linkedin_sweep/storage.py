from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from linkedin_sweep.models import CandidateItem
from linkedin_sweep.demo_data import seed_items

DATA_DIR = Path.home() / ".linkedin_sweep"
DATA_FILE = DATA_DIR / "items.json"
STATUS_FILE = DATA_DIR / "collector_status.json"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_items() -> list[CandidateItem]:
    ensure_data_dir()
    if not DATA_FILE.exists():
        items = seed_items()
        save_items(items)
        return items
    data = json.loads(DATA_FILE.read_text())
    return [CandidateItem.from_dict(item) for item in data]


def save_items(items: Iterable[CandidateItem]) -> None:
    ensure_data_dir()
    DATA_FILE.write_text(json.dumps([item.to_dict() for item in items], indent=2))


def update_item(item_id: str, **changes) -> CandidateItem | None:
    items = load_items()
    updated = None
    for item in items:
        if item.id == item_id:
            for key, value in changes.items():
                setattr(item, key, value)
            updated = item
            break
    save_items(items)
    return updated


def save_status(status: dict) -> None:
    ensure_data_dir()
    STATUS_FILE.write_text(json.dumps(status, indent=2))


def load_status() -> dict:
    ensure_data_dir()
    if not STATUS_FILE.exists():
        default = {
            "mode": "demo",
            "last_run": None,
            "last_result": "Demo mode active. Collector not configured yet.",
        }
        save_status(default)
        return default
    return json.loads(STATUS_FILE.read_text())
