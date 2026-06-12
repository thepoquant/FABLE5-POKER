# Phase 1 — Build Spec (verified against PokerKit 0.7.4)

This is the authoritative spec for the Phase 1 backend. All PokerKit API calls
below were verified by direct introspection on this machine (Python 3.13.13,
pokerkit 0.7.4), not guessed.

## Goal
A headless, in-memory, heads-up (2-player) No-Limit Texas Hold'em FastAPI
service. No AI, no database. Must be fully curl-testable.

## Verified PokerKit facts (do not deviate)
- Construct with `NoLimitTexasHoldem.create_state(automations, True, 0, (1, 2), 2, 200, 2)`
  where the args are: automations tuple, uniform-antes bool, antes (0), blinds (1,2),
  min-bet (2), starting stacks (200), player count (2).
- Automations MUST include `HOLE_DEALING` and `BOARD_DEALING` so cards are dealt
  automatically and streets self-advance. Full tuple:
  ANTE_POSTING, BET_COLLECTION, BLIND_OR_STRADDLE_POSTING, CARD_BURNING,
  HOLE_DEALING, BOARD_DEALING, HOLE_CARDS_SHOWING_OR_MUCKING, HAND_KILLING,
  CHIPS_PUSHING, CHIPS_PULLING.
- After construction, hole cards are already dealt and `actor_index` points at the
  first player to act. No manual deal calls needed.
- State inspection:
  - `state.status` -> True while hand in progress, False when hand is over.
  - `state.actor_index` -> int index of player to act, or None when no action pending.
  - `state.street_index` -> 0 preflop; use len(state.board_cards) to name the street
    (0=preflop, 3=flop, 4=turn, 5=river).
  - `state.hole_cards` -> list per player of card objects; str() them (e.g. '3c').
  - `state.board_cards` -> list of card objects; str() them.
  - `state.stacks` -> list of remaining stack per player.
  - `state.bets` -> list of current committed bet per player this street.
- Legal actions for the current actor:
  - `state.can_fold()` -> bool
  - `state.can_check_or_call()` -> bool; amount = `state.checking_or_calling_amount`
  - `state.can_complete_bet_or_raise_to()` -> bool;
    min = `state.min_completion_betting_or_raising_to_amount`,
    max = `state.max_completion_betting_or_raising_to_amount`
- Apply actions: `state.fold()`, `state.check_or_call()`,
  `state.complete_bet_or_raise_to(amount)`.

## Files
- `backend/engine.py` — PokerKit wrapper: new_game(), serialize_state(state, reveal_bot=False),
  apply_action(state, action, amount=None). Constants at top: SMALL_BLIND=1, BIG_BLIND=2,
  MIN_BET=2, STARTING_STACK=200.
- `backend/main.py` — FastAPI app, in-memory dict of sessions keyed by session_id.
  Endpoints: POST /new-game, GET /state/{id}, POST /action/{id} (body {action, amount?}),
  GET /health. CORS all origins.
- `backend/README.md` — run + curl instructions.

## Serialized public view (serialize_state returns)
street (str), board (list[str]), player_hole (list[str], seat 0),
bot_hole (list[str] or null unless reveal_bot), pot (int total of stacks committed),
stacks (list[int]), actor_index (int or null), hand_over (bool, = not state.status),
legal_actions (dict built from the can_* checks above), and when hand_over,
final stacks + per-player winnings delta vs starting stack.

## Player/bot seats
Seat 0 = human player, seat 1 = bot. (Bot is not auto-driven in Phase 1.)
