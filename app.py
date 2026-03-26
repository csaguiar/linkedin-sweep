from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import streamlit as st

from linkedin_sweep.collector import collect_demo_items, collect_from_linkedin_session, import_manual_items
from linkedin_sweep.storage import load_items, load_status, update_item

st.set_page_config(page_title="LinkedIn Sweep", layout="wide")

st.title("LinkedIn Sweep")
st.caption("Approval-first LinkedIn triage dashboard. Local-only by design.")

with st.sidebar:
    st.subheader("Collector")
    if st.button("Refresh demo items"):
        collect_demo_items()
        st.success("Demo items refreshed.")
    if st.button("Probe LinkedIn collector"):
        status = collect_from_linkedin_session()
        st.info(status["last_result"])

    st.markdown("---")
    status = load_status()
    st.subheader("Collector status")
    st.write(f"**Mode:** {status.get('mode', 'unknown')}")
    st.write(f"**Last run:** {status.get('last_run', 'never')}")
    st.write(status.get("last_result", "No status yet."))

items = load_items()

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    query = st.text_input("Filter by author/text")
with col2:
    status_filter = st.selectbox("Status", ["all", "pending", "approved", "rejected", "done"])
with col3:
    action_filter = st.selectbox("Action", ["all", "like", "comment", "repost", "reply", "ignore"])

filtered = []
for item in items:
    hay = f"{item.author} {item.text} {item.reason}".lower()
    if query and query.lower() not in hay:
        continue
    if status_filter != "all" and item.status != status_filter:
        continue
    if action_filter != "all" and item.suggested_action != action_filter:
        continue
    filtered.append(item)

st.subheader(f"Queue ({len(filtered)} items)")
for item in sorted(filtered, key=lambda x: x.score, reverse=True):
    with st.container(border=True):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown(f"### {item.author}")
            st.write(item.text)
            if item.url:
                st.markdown(f"[Open item]({item.url})")
        with c2:
            st.metric("Score", f"{item.score:.2f}")
            st.write(f"**Suggested:** {item.suggested_action}")
            st.write(f"**Status:** {item.status}")
            st.write(f"**Source:** {item.source}")

        st.write(f"**Why:** {item.reason}")
        if item.draft_comment:
            st.text_area("Draft", value=item.draft_comment, key=f"draft_{item.id}", height=90)

        notes_value = st.text_input("Notes", value=item.notes, key=f"notes_{item.id}")
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            if st.button("Approve", key=f"approve_{item.id}"):
                update_item(item.id, status="approved", notes=notes_value)
                st.rerun()
        with a2:
            if st.button("Reject", key=f"reject_{item.id}"):
                update_item(item.id, status="rejected", notes=notes_value)
                st.rerun()
        with a3:
            if st.button("Done", key=f"done_{item.id}"):
                update_item(item.id, status="done", notes=notes_value)
                st.rerun()
        with a4:
            if st.button("Reset", key=f"reset_{item.id}"):
                update_item(item.id, status="pending", notes=notes_value)
                st.rerun()

st.markdown("---")
st.subheader("Manual import")
st.caption("Paste CSV rows with columns: author,text,url")
manual_csv = st.text_area("Import CSV")
if st.button("Import rows"):
    if manual_csv.strip():
        from io import StringIO
        frame = pd.read_csv(StringIO(manual_csv))
        count = import_manual_items(frame.to_dict(orient="records"))
        st.success(f"Imported {count} items.")
        st.rerun()
    else:
        st.warning("Paste some CSV rows first.")

st.markdown("---")
st.warning(
    "This MVP is approval-first. It does not auto-post to LinkedIn. Browser automation for collection/execution should run on your own machine and may be brittle or account-risky if abused."
)
