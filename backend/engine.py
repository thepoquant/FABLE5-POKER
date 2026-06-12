from pokerkit import Automation, NoLimitTexasHoldem

SMALL_BLIND = 1
BIG_BLIND = 2
MIN_BET = 2
STARTING_STACK = 200

_AUTOMATIONS = (
    Automation.ANTE_POSTING,
    Automation.BET_COLLECTION,
    Automation.BLIND_OR_STRADDLE_POSTING,
    Automation.CARD_BURNING,
    Automation.HOLE_DEALING,
    Automation.BOARD_DEALING,
    Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
    Automation.HAND_KILLING,
    Automation.CHIPS_PUSHING,
    Automation.CHIPS_PULLING,
)

_STREET_NAMES = {0: "preflop", 3: "flop", 4: "turn", 5: "river"}


def new_game():
    state = NoLimitTexasHoldem.create_state(
        _AUTOMATIONS,
        True,
        0,
        (SMALL_BLIND, BIG_BLIND),
        MIN_BET,
        STARTING_STACK,
        2,
    )
    return state


def _card_str(card):
    return repr(card)


def _board_cards(state):
    return [_card_str(group[0]) for group in state.board_cards]


def serialize_state(state, reveal_bot=False):
    board_len = len(state.board_cards)
    street = _STREET_NAMES.get(board_len, "preflop")

    result = {
        "street": street,
        "board": _board_cards(state),
        "player_hole": [_card_str(c) for c in state.hole_cards[0]],
        "bot_hole": (
            [_card_str(c) for c in state.hole_cards[1]]
            if reveal_bot
            else None
        ),
        "stacks": list(state.stacks),
        "bets": list(state.bets),
        "current_street_bets": sum(state.bets),
        "total_pot": STARTING_STACK * 2 - sum(state.stacks),
        "actor_index": state.actor_index,
        "hand_over": not state.status,
    }

    if not state.status:
        result["legal_actions"] = None
        result["final_stacks"] = list(state.stacks)
        result["winnings"] = [s - STARTING_STACK for s in state.stacks]
    else:
        result["actor_index"] = state.actor_index
        if state.actor_index is not None:
            legal = {}
            if state.can_fold():
                legal["fold"] = True
            if state.can_check_or_call():
                legal["check_or_call"] = {
                    "amount": state.checking_or_calling_amount
                }
            if state.can_complete_bet_or_raise_to():
                legal["bet_or_raise"] = {
                    "min": state.min_completion_betting_or_raising_to_amount,
                    "max": state.max_completion_betting_or_raising_to_amount,
                }
            result["legal_actions"] = legal
        else:
            result["legal_actions"] = None

    return result


def apply_action(state, action, amount=None):
    if action == "fold":
        if not state.can_fold():
            raise ValueError("Fold is not a legal action")
        state.fold()
    elif action == "check_or_call":
        if not state.can_check_or_call():
            raise ValueError("Check or call is not a legal action")
        state.check_or_call()
    elif action == "bet_or_raise":
        if amount is None:
            raise ValueError("Amount is required for bet_or_raise")
        if not state.can_complete_bet_or_raise_to():
            raise ValueError("Bet or raise is not a legal action")
        state.complete_bet_or_raise_to(amount)
    else:
        raise ValueError(f"Unknown action: {action}")
