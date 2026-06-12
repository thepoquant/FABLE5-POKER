# Phase 1 Backend — Poker Engine + FastAPI

A headless, in-memory, heads-up (2-player) No-Limit Texas Hold'em service.
No AI, no database.

## Setup

```bash
cd backend
.venv\Scripts\activate
```

## Run

```bash
uvicorn main:app --reload
```

Server starts at `http://127.0.0.1:8000`.

## Endpoints

### POST /new-game

```bash
curl -s http://127.0.0.1:8000/new-game -X POST | python -m json.tool
```

### GET /state/{session_id}

```bash
curl -s http://127.0.0.1:8000/state/<SESSION_ID> | python -m json.tool
```

### POST /action/{session_id} — fold

```bash
curl -s http://127.0.0.1:8000/action/<SESSION_ID> -X POST -H "Content-Type: application/json" -d '{"action": "fold"}' | python -m json.tool
```

### POST /action/{session_id} — bet or raise

```bash
curl -s http://127.0.0.1:8000/action/<SESSION_ID> -X POST -H "Content-Type: application/json" -d '{"action": "bet_or_raise", "amount": 20}' | python -m json.tool
```

### GET /health

```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```
