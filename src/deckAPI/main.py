from random import choice
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Deck(BaseModel):
    deck: list[str]

    def to_json(self):
        return {
            "deck": self.deck
        }

@app.get("/{game_id}/deal")
async def deal_card(game_id:int):
    card = None
    with open('game_state.json', 'r') as openfile:
        state = json.load(openfile)
    if len(state['deck']) > 0:
        card = choice(state['deck'])
        if card in state['deck']:
            state['deck'].remove(card)
            with open('game_state.json', 'w') as f:
                json.dump(state, f)
    return {"card": card}

@app.post("/{game_id}/new-deck")
async def new_game(game_id:int, deck: Deck):
    with open('game_state.json', 'w') as f:
        json.dump(deck.to_json(), f)

    return {"game_id": game_id, "deck": deck}
