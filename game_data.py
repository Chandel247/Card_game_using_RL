from typing import List
from cards import MonsterCard, EffectCard, EffectTarget

def create_monster_deck() -> List[MonsterCard]:
    """Create 20 unique monster cards"""
    monsters = [
        MonsterCard(0, "Fire Dragon", 100, 25, 5),
        MonsterCard(1, "Ice Wolf", 80, 20, 8),
        MonsterCard(2, "Thunder Bird", 70, 30, 3),
        MonsterCard(3, "Earth Golem", 120, 15, 12),
        MonsterCard(4, "Shadow Assassin", 60, 35, 2),
        MonsterCard(5, "Light Guardian", 110, 18, 10),
        MonsterCard(6, "Water Serpent", 85, 22, 6),
        MonsterCard(7, "Wind Hawk", 75, 28, 4),
        MonsterCard(8, "Poison Scorpion", 65, 32, 3),
        MonsterCard(9, "Rock Titan", 130, 12, 15),
        MonsterCard(10, "Flame Phoenix", 90, 26, 5),
        MonsterCard(11, "Frost Bear", 95, 20, 9),
        MonsterCard(12, "Storm Eagle", 70, 30, 4),
        MonsterCard(13, "Nature Treant", 115, 16, 11),
        MonsterCard(14, "Dark Reaper", 55, 38, 1),
        MonsterCard(15, "Holy Paladin", 105, 19, 10),
        MonsterCard(16, "Ocean Kraken", 100, 24, 7),
        MonsterCard(17, "Sky Griffin", 80, 27, 5),
        MonsterCard(18, "Venom Spider", 60, 33, 2),
        MonsterCard(19, "Mountain Giant", 140, 14, 14),
    ]
    return monsters

def create_effect_deck() -> List[EffectCard]:
    """Create 15 effect cards with temporary buffs"""
    effects = [
        # Damage effects
        EffectCard(0, "Fireball", 3, EffectTarget.OPPONENT_MONSTER, damage=20),
        EffectCard(1, "Lightning Strike", 4, EffectTarget.OPPONENT_MONSTER, damage=30),
        EffectCard(2, "Ice Shard", 2, EffectTarget.OPPONENT_MONSTER, damage=15),
        EffectCard(3, "Meteor", 5, EffectTarget.OPPONENT_MONSTER, damage=40),
        
        # Healing effects
        EffectCard(4, "Heal", 2, EffectTarget.SELF_MONSTER, heal=20),
        EffectCard(5, "Greater Heal", 4, EffectTarget.SELF_MONSTER, heal=40),
        EffectCard(6, "Regeneration", 3, EffectTarget.SELF_MONSTER, heal=25),
        
        # Buff effects (now temporary with duration)
        EffectCard(7, "Power Up", 3, EffectTarget.SELF_MONSTER, buff_attack=10, buff_duration=3),
        EffectCard(8, "Shield", 2, EffectTarget.SELF_MONSTER, buff_defense=8, buff_duration=3),
        EffectCard(9, "Rage", 4, EffectTarget.SELF_MONSTER, buff_attack=15, buff_duration=2),
        EffectCard(10, "Fortify", 3, EffectTarget.SELF_MONSTER, buff_defense=12, buff_duration=3),
        
        # Mixed effects
        EffectCard(11, "Drain", 4, EffectTarget.OPPONENT_MONSTER, damage=25, heal=15),
        EffectCard(12, "Empower", 5, EffectTarget.SELF_MONSTER, buff_attack=12, buff_defense=8, buff_duration=3),
        
        # Low cost effects
        EffectCard(13, "Quick Strike", 1, EffectTarget.OPPONENT_MONSTER, damage=10),
        EffectCard(14, "Rest", 1, EffectTarget.SELF_MONSTER, heal=10),
    ]
    return effects
