import numpy as np
import random
from typing import List, Tuple, Optional
from cards import MonsterCard, EffectCard, EffectTarget
from game_data import create_monster_deck, create_effect_deck
from colors import Colors

class MonsterCardGame:
    def __init__(self, max_energy: int = 10, energy_per_turn: int = 3):
        self.max_energy = max_energy
        self.energy_per_turn = energy_per_turn
        
        # Card pools
        self.all_monsters = create_monster_deck()
        self.all_effects = create_effect_deck()
        
        # Game state
        self.round_num = 0
        self.used_monster_ids = set()
        
        # Player states
        self.player_monsters: List[MonsterCard] = []
        self.player_active: Optional[int] = None
        self.player_energy = max_energy
        
        self.opponent_monsters: List[MonsterCard] = []
        self.opponent_active: Optional[int] = None
        self.opponent_energy = max_energy
        
        # Current turn
        self.current_player = 0  # 0 = player, 1 = opponent
        self.available_effects: List[EffectCard] = []
        self.turn_count = 0
        
    def start_new_round(self) -> bool:
        """Start a new round. Returns False if no more rounds available."""
        if self.round_num >= 3:
            return False
        
        self.round_num += 1
        self.turn_count = 0
        
        # Get available monsters (not used in previous rounds)
        available_monsters = [m for m in self.all_monsters if m.card_id not in self.used_monster_ids]
        
        if len(available_monsters) < 6:
            return False
        
        # Randomly assign 3 monsters to each player
        random.shuffle(available_monsters)
        self.player_monsters = [m.copy() for m in available_monsters[:3]]
        self.opponent_monsters = [m.copy() for m in available_monsters[3:6]]
        
        # Mark these monsters as used
        for m in available_monsters[:6]:
            self.used_monster_ids.add(m.card_id)
        
        # Reset HP and buffs for all monsters
        for m in self.player_monsters + self.opponent_monsters:
            m.reset_hp()
        
        # Reset energy
        self.player_energy = self.max_energy
        self.opponent_energy = self.max_energy
        
        # Reset active monsters
        self.player_active = None
        self.opponent_active = None
        
        # Player starts first
        self.current_player = 0
        
        return True
    
    def select_starting_monster(self, player: int, monster_idx: int) -> bool:
        """Select which monster to start the battle with"""
        if player == 0:
            if 0 <= monster_idx < len(self.player_monsters):
                self.player_active = monster_idx
                return True
        else:
            if 0 <= monster_idx < len(self.opponent_monsters):
                self.opponent_active = monster_idx
                return True
        return False
    
    def draw_effects(self):
        """Draw 3 random effect cards for current turn"""
        self.available_effects = random.sample(self.all_effects, 3)
    
    def get_legal_actions(self, player: int) -> List[int]:
        """Get legal actions for the player."""
        legal = [0]  # Can always pass
        
        energy = self.player_energy if player == 0 else self.opponent_energy
        
        # Effect card actions (1-3)
        for i, effect in enumerate(self.available_effects):
            if effect.energy_cost <= energy:
                legal.append(i + 1)
        
        # Switch monster actions (4-6)
        monsters = self.player_monsters if player == 0 else self.opponent_monsters
        active_idx = self.player_active if player == 0 else self.opponent_active
        
        for i in range(len(monsters)):
            if i != active_idx and monsters[i].is_alive():
                legal.append(i + 4)
        
        return legal
    
    def apply_effect(self, effect: EffectCard, player: int) -> str:
        """Apply an effect card"""
        if player == 0:
            self.player_energy -= effect.energy_cost
            my_monster = self.player_monsters[self.player_active]
            opp_monster = self.opponent_monsters[self.opponent_active]
        else:
            self.opponent_energy -= effect.energy_cost
            my_monster = self.opponent_monsters[self.opponent_active]
            opp_monster = self.player_monsters[self.player_active]
        
        messages = []
        
        if effect.target == EffectTarget.OPPONENT_MONSTER:
            dmg = opp_monster.take_damage(effect.damage)
            messages.append(f"Dealt {Colors.color_text(str(dmg), Colors.RED)} damage to {opp_monster.name}")
            if effect.heal > 0:
                my_monster.heal(effect.heal)
                messages.append(f"{my_monster.name} healed for {Colors.color_text(str(effect.heal), Colors.GREEN)}")
        
        elif effect.target == EffectTarget.SELF_MONSTER:
            if effect.heal > 0:
                my_monster.heal(effect.heal)
                messages.append(f"{my_monster.name} healed for {Colors.color_text(str(effect.heal), Colors.GREEN)}")
            
            if effect.buff_attack > 0 or effect.buff_defense > 0:
                my_monster.add_buff(effect.buff_attack, effect.buff_defense, effect.buff_duration, owner_player=player)
                buff_msg = []
                if effect.buff_attack > 0:
                    buff_msg.append(f"+{effect.buff_attack} ATK")
                if effect.buff_defense > 0:
                    buff_msg.append(f"+{effect.buff_defense} DEF")
                messages.append(f"{my_monster.name} gained {' and '.join(buff_msg)} for {effect.buff_duration} turns!")
        
        return " | ".join(messages)
    
    def execute_attack(self, attacker: MonsterCard, defender: MonsterCard) -> int:
        """Execute basic attack"""
        damage = defender.take_damage(attacker.attack)
        return damage
    
    def tick_all_buffs(self, current_player :int) -> List[str]:
        """Update all buff timers. Returns messages."""
        messages = []
        for monster in self.player_monsters + self.opponent_monsters:
            if monster.is_alive():
                messages.extend(monster.tick_buffs(current_player))
        return messages
    
    def step(self, player: int, action: int) -> Tuple[str, bool]:
        """Execute an action. Returns (message, turn_ended)"""
        if action == 0:  # Pass / Attack
            if player == 0:
                attacker = self.player_monsters[self.player_active]
                defender = self.opponent_monsters[self.opponent_active]
            else:
                attacker = self.opponent_monsters[self.opponent_active]
                defender = self.player_monsters[self.player_active]
            
            damage = self.execute_attack(attacker, defender)
            msg = f"{attacker.name} attacks {defender.name} for {Colors.color_text(str(damage), Colors.RED, True)} damage!"
            
            # Check if defender died
            if not defender.is_alive():
                msg += f"\n{Colors.error_color(defender.name + ' has been defeated!')}"
                # Try to switch to next alive monster automatically
                self._auto_switch_monster(1 - player)
            
            return msg, True
        
        elif 1 <= action <= 3:  # Play effect card
            effect_idx = action - 1
            effect = self.available_effects[effect_idx]
            msg = Colors.effect_color(f"Used {effect.name}! ") + self.apply_effect(effect, player)
            return msg, True  # Turn continues
        
        elif 4 <= action <= 6:  # Switch monster
            new_idx = action - 4
            if player == 0:
                self.player_active = new_idx
                msg = Colors.player_color(f"Switched to {self.player_monsters[new_idx].name}!")
            else:
                self.opponent_active = new_idx
                msg = Colors.opponent_color(f"Opponent switched to {self.opponent_monsters[new_idx].name}!")
            return msg, True  # Switching ends turn
        
        return "Invalid action", False
    
    def _auto_switch_monster(self, player: int):
        """Automatically switch to next alive monster"""
        monsters = self.player_monsters if player == 0 else self.opponent_monsters
        
        for i, monster in enumerate(monsters):
            if monster.is_alive():
                if player == 0:
                    self.player_active = i
                else:
                    self.opponent_active = i
                return
    
    def is_round_over(self) -> bool:
        """Check if current round is over"""
        player_alive = any(m.is_alive() for m in self.player_monsters)
        opponent_alive = any(m.is_alive() for m in self.opponent_monsters)
        return not (player_alive and opponent_alive)
    
    def get_round_winner(self) -> int:
        """Returns 0 for player, 1 for opponent, -1 for draw"""
        player_alive = any(m.is_alive() for m in self.player_monsters)
        opponent_alive = any(m.is_alive() for m in self.opponent_monsters)
        
        if player_alive and not opponent_alive:
            return 0
        elif opponent_alive and not player_alive:
            return 1
        else:
            return -1
    
    def next_turn(self):
        """Move to next player's turn"""
        # Tick buffs at end of turn
        buff_messages = self.tick_all_buffs(self.current_player)
        
        self.current_player = 1 - self.current_player
        self.turn_count += 1
        
        # Regenerate energy
        if self.current_player == 0:
            self.player_energy = min(self.max_energy, self.player_energy + self.energy_per_turn)
        else:
            self.opponent_energy = min(self.max_energy, self.opponent_energy + self.energy_per_turn)
        
        # Draw new effects
        self.draw_effects()
        
        return buff_messages
    
    def get_state_vector(self, player: int) -> np.ndarray:
        """Get state representation for RL agent including buffs"""
        state = []
        
        if player == 0:
            # Own state
            state.append(self.player_energy / self.max_energy)
            active = self.player_monsters[self.player_active]
            state.extend([
                active.hp / active.max_hp,
                active.attack / 50.0,
                active.defense / 20.0,
                len(active.active_buffs) / 5.0  # Normalized buff count
            ])
            
            # Other own monsters
            for i, m in enumerate(self.player_monsters):
                if i != self.player_active:
                    state.append(1.0 if m.is_alive() else 0.0)
                    state.append(m.hp / m.max_hp if m.is_alive() else 0.0)
            
            # Opponent active monster
            opp_active = self.opponent_monsters[self.opponent_active]
            state.extend([
                opp_active.hp / opp_active.max_hp,
                opp_active.attack / 50.0,
                opp_active.defense / 20.0
            ])
        else:
            # Flip perspective for opponent
            state.append(self.opponent_energy / self.max_energy)
            active = self.opponent_monsters[self.opponent_active]
            state.extend([
                active.hp / active.max_hp,
                active.attack / 50.0,
                active.defense / 20.0,
                len(active.active_buffs) / 5.0
            ])
            
            for i, m in enumerate(self.opponent_monsters):
                if i != self.opponent_active:
                    state.append(1.0 if m.is_alive() else 0.0)
                    state.append(m.hp / m.max_hp if m.is_alive() else 0.0)
            
            opp_active = self.player_monsters[self.player_active]
            state.extend([
                opp_active.hp / opp_active.max_hp,
                opp_active.attack / 50.0,
                opp_active.defense / 20.0
            ])
        
        # Available effects
        for effect in self.available_effects:
            state.append(effect.energy_cost / self.max_energy)
            state.append(effect.damage / 50.0 if effect.damage > 0 else 0.0)
            state.append(effect.heal / 50.0 if effect.heal > 0 else 0.0)
        
        # Round number and turn count
        state.append(self.round_num / 3.0)
        state.append(min(self.turn_count / 50.0, 1.0))
        
        return np.array(state, dtype=np.float32)
