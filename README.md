# CommitCast

A bot that turns your GitHub commit activity into casual "build in public" style tweets and sends them to a Telegram channel every morning.

## How it works

1. **Fetch** — Pulls recent `PushEvent`s from the GitHub API (up to 3 days back)
2. **Summarize** — For each push, fetches the raw diff and uses an LLM (via OpenRouter) to write a one-sentence plain-English summary of what changed
3. **Tweet** — Groups summaries by repo + date and feeds them to an LLM with a curated persona prompt ("CS student building real projects, dry wit, no hustle-bro energy") to produce 1–3 tweet options per group
4. **Post** — Sends the generated tweets to a Telegram channel via the Bot API (Markdown formatted)

## Tech stack

- **Python 3.11** — core logic
- **OpenRouter** — LLM proxy (fallback model: `openrouter/free`, preferred: `qwen/qwen3-coder:free`)
- **GitHub API** — events, compare, and repo endpoints (no auth, public data only)
- **Telegram Bot API** — message delivery
- **uv** — package management

## Setup

```bash
uv sync
```

Create a `.env` file:

```
API_KEY=sk-or-v1-...          # OpenRouter API key
TELEGRAM_BOT_TOKEN=...        # Telegram bot token
TELEGRAM_CHAT_ID=...          # Telegram chat/channel ID
```

## Usage

```bash
python main.py
```

The script will fetch activity, generate tweets, print them to stdout, and post them to Telegram.

## Scheduling

Add a cron job to run it daily:

```cron
0 8 * * * cd /path/to/commitcast && python main.py
```

## Project structure

| File | Role |
|---|---|
| `main.py` | Entry point — orchestrates fetch → summarize → tweet → post |
| `getdata.py` | Fetches GitHub PushEvents, diffs, and repo metadata |
| `llm.py` | OpenRouter wrapper with model fallback and diff summarizer |
| `twitter.py` | Persona-driven tweet generation from grouped summaries |

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `API_KEY` | Yes | OpenRouter API key |
| `TELEGRAM_BOT_TOKEN` | Yes | Telegram bot token |
| `TELEGRAM_CHAT_ID` | Yes | Target chat/channel ID |