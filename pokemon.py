from pokemontcgsdk import Set, Card
import random
from typing import List
from flask import Flask

not_rares = ["Common", "Uncommon", "Promo"]
app = Flask(__name__)


def get_random_booster() -> List[Card]:
    set = get_random_set()
    set_cards = Card.where(q=f"set.id:{set.id}")
    commons = list(filter(lambda card: card.rarity == "Common", set_cards))
    uncommons = list(filter(lambda card: card.rarity == "Uncommon", set_cards))
    rares = list(filter(lambda card: card.rarity not in not_rares, set_cards))

    if min(len(commons), len(uncommons), len(rares)) < 1:
        print(f"Error found this set: {set}")
        return None

    return random.choices(commons, weights=None, k=6) + random.choices(
        uncommons, weights=None, k=3) + [random.choice(rares)]


def get_random_set() -> Set:
    all_sets = Set.all()
    return random.choice(all_sets)
