class Card:
    def __init__(self, id:int, name:str, cost:int, card_type:str, atk=None, defense=None, hp=None, effect_type=None, duration=None):
        self.id=id
        self.cost=cost
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

    def take_damage(self, amount:int)->int:
        if (self.defense<=amount):
            actual_dmg=min(self.hp,amount-self.defense)
            self.hp=max(0,self.hp-actual_dmg)
            return actual_dmg
        else:
            return 0
    
    def __str__(self):
        return (f"Id:{self.id}, Name:{self.name}, card_type:{self.card_type}, hp:{self.hp}, atk:{self.atk}, def:{self.defense}")
    
    def is_alive(self)->bool:
        return self.hp>0
    
card = Card(id=1, name="Test Dragon", cost=3, card_type="monster", 
                atk=10, defense=2, hp=15)
    
    # Test string representation
print(card)  # Should print nice format
    
    # Test take_damage
damage_taken = card.take_damage(5)
print(f"Damage taken: {damage_taken}, HP remaining: {card.hp}")
