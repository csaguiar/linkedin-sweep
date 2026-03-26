# LinkedIn Sweep

LinkedIn Sweep is a **local-only, approval-first** dashboard for reviewing potential LinkedIn engagement actions.

It is designed for a workflow where the system gathers candidate interactions, suggests what to do next, and leaves the final decision to you.

## What it does

- Shows a queue of candidate LinkedIn items
- Suggests actions like:
  - `like`
  - `comment`
  - `repost`
  - `reply`
  - `ignore`
- Lets you mark items as:
  - `pending`
  - `approved`
  - `rejected`
  - `done`
- Stores state locally in `~/.linkedin_sweep/`
- Starts in **demo mode** so the dashboard is usable immediately

## Current MVP scope

This MVP is intentionally conservative.

- ✅ Local Streamlit dashboard
- ✅ Local persistence
- ✅ Demo queue with seeded records
- ✅ Manual import of candidate items via CSV paste
- ✅ Collector status panel
- ✅ Architecture ready for a future Playwright collector
- ✅ uv-based project management
- ❌ No automatic posting by default
- ❌ No full LinkedIn scraping implementation yet

## Why no full LinkedIn automation by default?

Because LinkedIn automation is fragile and can be risky.

Issues include:
- DOM/selectors change often
- login/captcha/checkpoint flows can break bots
- aggressive automation may create account risk
- comments/replies posted in your name should stay behind approval unless you explicitly choose otherwise

## Suggested architecture

- **Streamlit UI**: review and approve action items
- **Storage**: local JSON now, easy to upgrade to SQLite
- **Collector**: Playwright-based browser automation running on your own machine
- **Executor**: optional future module that performs approved actions after explicit confirmation

## Project structure

```text
linkedin-sweep/
├── app.py
├── pyproject.toml
├── README.md
└── src/
    └── linkedin_sweep/
        ├── __init__.py
        ├── collector.py
        ├── demo_data.py
        ├── models.py
        ├── scoring.py
        └── storage.py
```

## Setup

From the project directory:

```bash
uv sync
```

If you plan to add Playwright collection later:

```bash
uv run playwright install chromium
```

## Run

```bash
uv run streamlit run app.py
```

Then open the local URL shown by Streamlit.

## Manual import

In the app, use the **Manual import** section and paste CSV rows with columns:

```csv
author,text,url
Jane Doe,"Interesting post about LLM evaluation in production",https://www.linkedin.com/feed/update/...
```

Imported rows are scored and added to the queue.

## Local data

The app stores data in:

- `~/.linkedin_sweep/items.json`
- `~/.linkedin_sweep/collector_status.json`

## Next logical step

Implement a real Playwright collector that:
- runs on a machine you control
- reuses a real browser profile/session
- collects feed items / notifications / inbox candidates
- writes normalized queue items into local storage

## Notes

This tool is meant to help you decide what deserves attention. The sane version is:
1. collect candidate items
2. recommend actions
3. approve manually
4. only then execute anything in your name
