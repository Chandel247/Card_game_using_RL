import numpy as np
import random
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional
from game_engine import MonsterCardGame
from colors import Colors

# ========== Q-Learning Agent ==========
class QLearningAgent:
    """Q-learning based agent"""
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.3, name="Q-Agent"):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.name = name
        
        self.q_table: Dict[str, Dict[int, float]] = defaultdict(lambda: defaultdict(float))
        self.experience_buffer: List[Tuple] = []
        
        self.base_epsilon = epsilon
        self.round_modifiers = {1: 1.0, 2: 0.7, 3: 0.4}
        
        self.games_played = 0
        self.rounds_won = 0
        self.rounds_lost = 0
    
    def get_state_key(self, state_vector: np.ndarray) -> str:
        """Convert state vector to hashable key"""
        discretized = (state_vector * 10).astype(int)
        return str(discretized.tolist())
    
    def choose_action(self, game: MonsterCardGame, player: int, round_num: int = 1) -> int:
        """Choose action using epsilon-greedy policy"""
        legal_actions = game.get_legal_actions(player)
        state = game.get_state_vector(player)
        state_key = self.get_state_key(state)
        
        current_epsilon = self.base_epsilon * self.round_modifiers.get(round_num, 0.3)
        
        if random.random() < current_epsilon:
            return random.choice(legal_actions)
        else:
            q_values = {a: self.q_table[state_key][a] for a in legal_actions}
            if not q_values or all(v == 0 for v in q_values.values()):
                return random.choice(legal_actions)
            return max(q_values, key=q_values.get)
    
    def update(self, state: np.ndarray, action: int, reward: float, 
               next_state: np.ndarray, done: bool):
        """Update Q-values"""
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        current_q = self.q_table[state_key][action]
        
        if done:
            target_q = reward
        else:
            next_max_q = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0
            target_q = reward + self.gamma * next_max_q
        
        self.q_table[state_key][action] = current_q + self.lr * (target_q - current_q)
        self.experience_buffer.append((state, action, reward, next_state, done))
    
    def learn_from_player(self, player_action: int, game_state: np.ndarray):
        """Learn from observing player actions"""
        state_key = self.get_state_key(game_state)
        self.q_table[state_key][player_action] += 0.05
    
    def save(self, filename: str):
        """Save agent's Q-table"""
        data = {
            'q_table': dict(self.q_table),
            'games_played': self.games_played,
            'rounds_won': self.rounds_won,
            'rounds_lost': self.rounds_lost,
            'lr': self.lr,
            'gamma': self.gamma,
            'epsilon': self.epsilon,
            'name': self.name
        }
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        print(Colors.success_color(f"Agent saved to {filename}"))
    
    def load(self, filename: str):
        """Load agent's Q-table"""
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            self.q_table = defaultdict(lambda: defaultdict(float), data['q_table'])
            self.games_played = data.get('games_played', 0)
            self.rounds_won = data.get('rounds_won', 0)
            self.rounds_lost = data.get('rounds_lost', 0)
            self.name = data.get('name', self.name)
            print(Colors.success_color(f"Agent '{self.name}' loaded from {filename}"))
            print(f"Stats: {self.games_played} games, {self.rounds_won} wins, {self.rounds_lost} losses")
            return True
        except FileNotFoundError:
            print(Colors.error_color(f"File {filename} not found"))
            return False


# ========== Deep Q-Network Agent ==========
class DQNetwork(nn.Module):
    """Deep Q-Network for action-value approximation"""
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 128):
        super(DQNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc4 = nn.Linear(hidden_size, action_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

class DQNAgent:
    """Deep Q-Network agent with experience replay"""
    def __init__(self, state_size: int = 23, action_size: int = 7, 
                 learning_rate: float = 0.001, discount_factor: float = 0.95,
                 epsilon: float = 0.5, epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.1, name: str = "DQN-Agent"):
        
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.name = name
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Q-Networks
        self.policy_net = DQNetwork(state_size, action_size).to(self.device)
        self.target_net = DQNetwork(state_size, action_size).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=learning_rate)
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        
        self.round_modifiers = {1: 1.0, 2: 0.7, 3: 0.4}
        
        self.games_played = 0
        self.rounds_won = 0
        self.rounds_lost = 0
        self.update_counter = 0
        self.target_update = 100
    
    def choose_action(self, game: MonsterCardGame, player: int, round_num: int = 1) -> int:
        """Choose action using epsilon-greedy with neural network"""
        legal_actions = game.get_legal_actions(player)
        state = game.get_state_vector(player)
        
        current_epsilon = self.epsilon * self.round_modifiers.get(round_num, 0.3)
        
        if random.random() < current_epsilon:
            return random.choice(legal_actions)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.policy_net(state_tensor).cpu().numpy()[0]
            
            # Mask illegal actions
            masked_q = {a: q_values[a] for a in legal_actions}
            return max(masked_q, key=masked_q.get)
    
    def update(self, state: np.ndarray, action: int, reward: float,
               next_state: np.ndarray, done: bool):
        """Store experience and train network"""
        self.memory.append((state, action, reward, next_state, done))
        
        if len(self.memory) < self.batch_size:
            return
        
        # Sample batch
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        
        # Current Q values
        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Target Q values
        with torch.no_grad():
            next_q = self.target_net(next_states).max(1)[0]
            target_q = rewards + (1 - dones) * self.gamma * next_q
        
        # Loss and optimization
        loss = nn.MSELoss()(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update target network
        self.update_counter += 1
        if self.update_counter % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def learn_from_player(self, player_action: int, game_state: np.ndarray):
        """Learn from player (could implement imitation learning)"""
        pass
    
    def save(self, filename: str):
        """Save DQN model"""
        torch.save({
            'policy_net': self.policy_net.state_dict(),
            'target_net': self.target_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'games_played': self.games_played,
            'rounds_won': self.rounds_won,
            'rounds_lost': self.rounds_lost,
            'name': self.name
        }, filename)
        print(Colors.success_color(f"DQN Agent saved to {filename}"))
    
    def load(self, filename: str):
        """Load DQN model"""
        try:
            checkpoint = torch.load(filename, map_location=self.device)
            self.policy_net.load_state_dict(checkpoint['policy_net'])
            self.target_net.load_state_dict(checkpoint['target_net'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            self.epsilon = checkpoint['epsilon']
            self.games_played = checkpoint.get('games_played', 0)
            self.rounds_won = checkpoint.get('rounds_won', 0)
            self.rounds_lost = checkpoint.get('rounds_lost', 0)
            self.name = checkpoint.get('name', self.name)
            print(Colors.success_color(f"DQN Agent '{self.name}' loaded from {filename}"))
            print(f"Stats: {self.games_played} games, {self.rounds_won} wins")
            return True
        except FileNotFoundError:
            print(Colors.error_color(f"File {filename} not found"))
            return False


# ========== Strategic Rule-Based Agents ==========
class AggressiveAgent:
    """Aggressive rule-based agent - focuses on damage"""
    def __init__(self, name="Aggressive-Bot"):
        self.name = name
        self.games_played = 0
        self.rounds_won = 0
        self.rounds_lost = 0
    
    def choose_action(self, game: MonsterCardGame, player: int, round_num: int = 1) -> int:
        legal_actions = game.get_legal_actions(player)
        state = game.get_state_vector(player)
        
        my_hp_idx = 1
        opp_hp_idx = 7
        energy_idx = 0
        
        my_hp = state[my_hp_idx]
        opp_hp = state[opp_hp_idx]
        energy = state[energy_idx]
        
        # Prefer high damage effects when available
        damage_actions = [1, 2, 3, 4]  # Effect cards
        available_damage = [a for a in legal_actions if a in damage_actions]
        
        if available_damage and energy > 0.3:
            # Choose highest cost (usually highest damage)
            return max(available_damage)
        
        # If low HP and can switch to healthier monster
        if my_hp < 0.4:
            switch_actions = [a for a in legal_actions if a >= 4]
            if switch_actions:
                return random.choice(switch_actions)
        
        return 0  # Attack
    
    def update(self, *args, **kwargs):
        pass
    
    def learn_from_player(self, *args, **kwargs):
        pass


class DefensiveAgent:
    """Defensive rule-based agent - focuses on survival"""
    def __init__(self, name="Defensive-Bot"):
        self.name = name
        self.games_played = 0
        self.rounds_won = 0
        self.rounds_lost = 0
    
    def choose_action(self, game: MonsterCardGame, player: int, round_num: int = 1) -> int:
        legal_actions = game.get_legal_actions(player)
        state = game.get_state_vector(player)
        
        my_hp_idx = 1
        energy_idx = 0
        
        my_hp = state[my_hp_idx]
        energy = state[energy_idx]
        
        # If low HP, prioritize healing
        if my_hp < 0.5 and energy > 0.2:
            heal_actions = [5, 6, 7]  # Heal effects typically
            available_heal = [a for a in legal_actions if a in heal_actions]
            if available_heal:
                return random.choice(available_heal)
        
        # Switch to fresh monster if current is damaged
        if my_hp < 0.3:
            switch_actions = [a for a in legal_actions if a >= 4]
            if switch_actions:
                return random.choice(switch_actions)
        
        # Otherwise attack or use buff
        return 0
    
    def update(self, *args, **kwargs):
        pass
    
    def learn_from_player(self, *args, **kwargs):
        pass


class BalancedAgent:
    """Balanced rule-based agent - adapts to situation"""
    def __init__(self, name="Balanced-Bot"):
        self.name = name
        self.games_played = 0
        self.rounds_won = 0
        self.rounds_lost = 0
    
    def choose_action(self, game: MonsterCardGame, player: int, round_num: int = 1) -> int:
        legal_actions = game.get_legal_actions(player)
        state = game.get_state_vector(player)
        
        my_hp_idx = 1
        opp_hp_idx = 7
        energy_idx = 0
        
        my_hp = state[my_hp_idx]
        opp_hp = state[opp_hp_idx]
        energy = state[energy_idx]
        
        # Critical HP - heal or switch
        if my_hp < 0.3:
            heal_actions = [a for a in legal_actions if a in [5, 6, 7]]
            if heal_actions and energy > 0.2:
                return random.choice(heal_actions)
            switch_actions = [a for a in legal_actions if a >= 4]
            if switch_actions:
                return random.choice(switch_actions)
        
        # Opponent low HP - go for kill
        if opp_hp < 0.4:
            damage_actions = [a for a in legal_actions if a in [1, 2, 3, 4]]
            if damage_actions and energy > 0.2:
                return max(damage_actions)
        
        # Good HP - use buffs if available
        if my_hp > 0.6 and energy > 0.3:
            buff_actions = [a for a in legal_actions if a in [7, 8, 9, 10]]
            if buff_actions:
                return random.choice(buff_actions)
        
        # Default to attack
        return 0
    
    def update(self, *args, **kwargs):
        pass
    
    def learn_from_player(self, *args, **kwargs):
        pass
