from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

from engine import new_game, serialize_state, apply_action

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, object] = {}


class ActionBody(BaseModel):
    action: str
    amount: int | None = None


@app.post("/new-game")
def create_game():
    state = new_game()
    session_id = uuid4().hex
    sessions[session_id] = state
    return {"session_id": session_id, "state": serialize_state(state)}


@app.get("/state/{session_id}")
def get_state(session_id: str):
    state = sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return serialize_state(state)


@app.post("/action/{session_id}")
def post_action(session_id: str, body: ActionBody):
    state = sessions.get(session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        apply_action(state, body.action, body.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return serialize_state(state)


@app.get("/health")
def health():
    return {"status": "ok"}
