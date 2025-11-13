from typing import Optional, List
import json
import os

class Card:
    def __init__(self, id:int, name:str, card_type:str, cost:Optional[int]=None, atk:Optional[int]=None, defense:Optional[int]=None, hp:Optional[int]=None, effect_type:Optional[str]=None, duration:Optional[int]=None):
        self.id=id
        self.card_type=card_type

        if (self.card_type=="monster"):
            self.name=name
            self.hp=hp
            self.max_hp=hp
            self.atk=atk
            self.defense=defense
        else:
            self.name=name
            self.effect_type=effect_type
            self.duration=duration
            self.cost=cost

    def take_damage(self, amount:int)->int:
        if (self.defense<amount):
            actual_dmg=min(self.hp,amount-self.defense)
            self.hp=max(0,self.hp-actual_dmg)
            return actual_dmg
        else:
            return 0
    
    def __str__(self):
        if (self.card_type=='monster'):
            return (f"Id:{self.id}, Name:{self.name}, HP:{self.hp}, Def:{self.defense}, Atk:{self.atk}")
        else:
            return (f"Id:{self.id}, Name:{self.name}, Cost:{self.cost}, Effect_type:{self.effect_type}, Duration:{self.duration}")

    def is_alive(self)->bool:
        return self.hp>0

def make_monster_pool():
    """Load all monster cards from data/monsters.json and return as a list of Card objects."""
    monsters_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'monsters.json')
    with open(file=monsters_path, mode="r") as file:
        data = json.load(file)
    
    monster_cards = []
    for monster in data:
        card = Card(
            id=monster['id'],
            name=monster['name'],
            card_type="monster",
            atk=monster.get('atk', 0),
            defense=monster.get('defense', 0),
            hp=monster.get('hp', 0)
        )
        monster_cards.append(card)
    return monster_cards

def make_effect_pool():
    """Load all effect cards from data/effects.json and return as a list of Card objects."""
    effects_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'effects.json')
    with open(file=effects_path, mode="r") as file:
        data = json.load(file)
    
    effect_cards = []
    for effect in data:
        card = Card(
            id=effect['id'],
            name=effect['name'],
            card_type="spell",
            cost=effect.get('cost', 0),
            effect_type=effect.get('effect_type', ''),
            duration=effect.get('duration', 0)
        )
        effect_cards.append(card)
    return effect_cards
