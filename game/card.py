from typing import Optional

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
        if (self.defense<=amount):
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
