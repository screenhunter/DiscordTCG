from typing import List
from flask import Flask
from flask_discord_interactions import DiscordInteractions
from replit import db
from pokemontcgsdk import Card

app = Flask(__name__)
discord = DiscordInteractions(app)


def get_user_data(discord_id: str):
    if not discord_id in db:
        db[discord_id] = {
            "id": discord_id,
            "pack_count": 0,
            "inventory": [],
        }
    return db[discord_id]


def add_pack(discord_id: str, pack: List[Card]):
    db[discord_id]["pack_count"] += 1
    db[discord_id]["inventory"].extend([card.id for card in pack])
