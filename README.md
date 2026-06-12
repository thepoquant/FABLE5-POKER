# Fable 5 Poker Trainer

Play-money heads-up Texas Hold'em trainer. The user plays against Claude Fable 5, which acts as both opponent and coach, teaching transferable poker fundamentals.

Co-owned product (Porter + Bluey). The associated Fable 5-themed token is a separate community/narrative layer and is intentionally kept legally and practically separate from this app.

## Structure

- `backend/` — FastAPI service wrapping the PokerKit engine (game state, actions). AI and ELO/leaderboard added in later phases.

## Build Phases

1. **PokerKit service** (foundation) — headless heads-up NLHE, curl-testable, no AI.
2. **Fable 5 as opponent** — model chooses its own actions.
3. **Fable 5 as coach** — independent review of the user's decisions (never leaks the bot's cards).
4. **ELO + leaderboard** — Postgres-backed ratings; reward hook stubbed.

## Status

Phase 1 — in progress.
