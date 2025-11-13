from typing import Optional, List
from .card import Card
import random as rand

class Player:
    def __init__(self, deck:List[Card]):
        self.hp=30
        self.max_hp=30
        self.defense=10
        self.mana=3
        self.deck=deck
        self.hand=[]
        self.bench=[]
        self.playing_card=None
    
    def draw_hand(self)-> List[Card]:
        for i in range(5):
            idx=rand.randint(0,len(self.deck))
            self.hand.append(self.deck.pop(idx))
        return self.hand

    def play_card(self, card_choice:int)->Card:
        if (card_choice<len(self.hand)):
            self.playing_card=self.hand[card_choice]
            self.hand.pop(card_choice)
            for card in self.hand:
                self.bench.append(card)
            return self.playing_card
        else:
            raise ValueError("Please select from available monsters")
        
    def take_damage(self, amount:int)->int:
        if (self.defense<amount):
            actual_dmg=min(self.hp,amount-self.defense)
            self.hp=max(0,self.hp-actual_dmg)
            return actual_dmg
        else:
            return 0
        
    def get_alive_monsters(self)->List[Card]:
        alive_monsters = []
        if self.playing_card is not None and self.playing_card.is_alive():
            alive_monsters.append(self.playing_card)
        for card in self.bench:
            if card.is_alive():
                alive_monsters.append(card)
        return alive_monsters