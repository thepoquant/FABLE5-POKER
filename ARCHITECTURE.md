# Architecture

## Overview

A play-money heads-up (2-player) No-Limit Texas Hold'em trainer. The user plays one-on-one against Claude Fable 5, which serves as both a challenging opponent and a coach that explains the user's mistakes and strengths in terms of transferable poker fundamentals.

## Design Principles

- **Engine is not hand-rolled.** The poker rules (dealing, betting rounds, legal-action validation, side pots, showdown, hand evaluation) come from PokerKit, a peer-reviewed open-source library. We do not reimplement poker logic.
- **Opponent and coach are separate calls.** The model's opponent decision and its coaching feedback are produced by distinct calls so coaching can never leak the bot's hole cards or strategy. The coach reasons about the user's decision on its own merits.
- **Play-money only.** No wagering, no real-value stakes inside the game.
- **App and token are separate.** The associated token is a community/narrative layer with no mechanical link to gameplay.

## Build Phases

| Phase | Scope |
|---|---|
| 1 | PokerKit FastAPI service — heads-up NLHE, in-memory game state, start-hand / get-state / submit-action endpoints. Headless, curl-testable, no AI. |
| 2 | Fable 5 as opponent — model receives legal game state, returns its action. |
| 3 | Fable 5 as coach — independent review pass on the user's decisions; fundamentals feedback. |
| 4 | ELO + public leaderboard (Postgres). Reward/airdrop hook stubbed only. |

## Tech Stack

- Python 3 / FastAPI
- PokerKit (poker engine)
- Claude Fable 5 API (opponent + coach) — later phase
- PostgreSQL via asyncpg (ELO + leaderboard) — later phase

## Phase 1 Decisions

- **Heads-up only** (2 players: user vs bot seat). No multi-seat table logic yet.
- **In-memory session state**: active games held in a dict keyed by session id. Games do not survive a server restart — acceptable for development. Migrate to a persistent store later without changing the endpoint contract.
