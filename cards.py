from enum import Enum
from typing import Optional, Dict

class EffectTarget(Enum):
    SELF_MONSTER = "self_monster"
    OPPONENT_MONSTER = "opponent_monster"
    SELF_PLAYER = "self_player"

class BuffEffect:
    """Represents a temporary buff effect on a monster"""
    def __init__(self, attack_buff: int = 0, defense_buff: int = 0, duration: int = 3, owner_player: int = 0):
        self.attack_buff = attack_buff
        self.defense_buff = defense_buff
        self.duration = duration
        self.turns_remaining = duration
        self.owner_player = owner_player
    
    def tick(self, current_player: int) -> bool:
        """Decrease turn counter. Returns True if effect should be removed."""
        if (self.owner_player == current_player):
            self.turns_remaining -= 1
        return self.turns_remaining <= 0
    
    def __repr__(self):
        buffs = []
        if self.attack_buff > 0:
            buffs.append(f"+{self.attack_buff}ATK")
        if self.defense_buff > 0:
            buffs.append(f"+{self.defense_buff}DEF")
        return f"{'/'.join(buffs)}({self.turns_remaining})"

class MonsterCard:
    def __init__(self, card_id: int, name: str, hp: int, attack: int, defense: int):
        self.card_id = card_id
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.base_defense = defense
        self.active_buffs: list[BuffEffect] = []
    
    @property
    def attack(self) -> int:
        """Current attack with buffs"""
        return self.base_attack + sum(buff.attack_buff for buff in self.active_buffs)
    
    @property
    def defense(self) -> int:
        """Current defense with buffs"""
        return self.base_defense + sum(buff.defense_buff for buff in self.active_buffs)
    
    def add_buff(self, attack_buff: int = 0, defense_buff: int = 0, duration: int = 3, owner_player: int = 0):
        """Add a temporary buff effect"""
        if attack_buff > 0 or defense_buff > 0:
            self.active_buffs.append(BuffEffect(attack_buff, defense_buff, duration, owner_player))
    
    def tick_buffs(self, current_player: int) -> list[str]:
        """Update buff timers and remove expired ones. Returns messages."""
        messages = []
        buffs_to_remove = []
        
        for buff in self.active_buffs:
            if buff.tick(current_player):
                buffs_to_remove.append(buff)
                messages.append(f"{self.name}'s buff expired!")
        
        for buff in buffs_to_remove:
            self.active_buffs.remove(buff)
        
        return messages
    
    def clear_buffs(self):
        """Remove all buffs"""
        self.active_buffs.clear()
    
    def take_damage(self, damage: int) -> int:
        """Apply damage after defense. Returns actual damage dealt."""
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def heal(self, amount: int):
        """Heal the monster, capped at max HP"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def reset_hp(self):
        """Reset HP to maximum and clear buffs"""
        self.hp = self.max_hp
        self.clear_buffs()
    
    def copy(self):
        """Create a copy of this monster"""
        return MonsterCard(self.card_id, self.name, self.max_hp, self.base_attack, self.base_defense)
    
    def get_buff_display(self) -> str:
        """Get display string for active buffs"""
        if not self.active_buffs:
            return ""
        return " [" + ", ".join(str(buff) for buff in self.active_buffs) + "]"
    
    def __repr__(self):
        from colors import Colors
        hp_color = Colors.hp_color(self.hp, self.max_hp)
        hp_str = Colors.color_text(f"HP:{self.hp}/{self.max_hp}", hp_color)
        atk_str = f"ATK:{self.attack}"
        def_str = f"DEF:{self.defense}"
        
        # Show base stats if buffed
        if self.active_buffs:
            if self.attack != self.base_attack:
                atk_str = Colors.color_text(f"ATK:{self.attack}({self.base_attack})", Colors.GREEN)
            if self.defense != self.base_defense:
                def_str = Colors.color_text(f"DEF:{self.defense}({self.base_defense})", Colors.GREEN)
        
        buff_display = Colors.color_text(self.get_buff_display(), Colors.MAGENTA) if self.active_buffs else ""
        
        return f"{Colors.BOLD}{self.name}{Colors.RESET} ({hp_str} {atk_str} {def_str}){buff_display}"

class EffectCard:
    def __init__(self, effect_id: int, name: str, energy_cost: int, 
                 target: EffectTarget, damage: int = 0, heal: int = 0, 
                 buff_attack: int = 0, buff_defense: int = 0, buff_duration: int = 3):
        self.effect_id = effect_id
        self.name = name
        self.energy_cost = energy_cost
        self.target = target
        self.damage = damage
        self.heal = heal
        self.buff_attack = buff_attack
        self.buff_defense = buff_defense
        self.buff_duration = buff_duration
    
    def __repr__(self):
        from colors import Colors
        effects = []
        if self.damage > 0: 
            effects.append(Colors.color_text(f"DMG:{self.damage}", Colors.RED))
        if self.heal > 0: 
            effects.append(Colors.color_text(f"HEAL:{self.heal}", Colors.GREEN))
        if self.buff_attack > 0: 
            effects.append(Colors.color_text(f"+ATK:{self.buff_attack}({self.buff_duration}t)", Colors.YELLOW))
        if self.buff_defense > 0: 
            effects.append(Colors.color_text(f"+DEF:{self.buff_defense}({self.buff_duration}t)", Colors.YELLOW))
        
        cost_str = Colors.color_text(f"Cost:{self.energy_cost}", Colors.CYAN)
        target_str = Colors.color_text(f"→{self.target.value}", Colors.BRIGHT_BLACK)
        
        return f"{Colors.BOLD}{self.name}{Colors.RESET} [{cost_str}] ({' '.join(effects)}) {target_str}"
