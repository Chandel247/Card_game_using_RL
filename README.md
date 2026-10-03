# Monster Card Game with Reinforcement Learning

A strategic turn-based card game featuring intelligent AI agents trained using reinforcement learning. Players command teams of monsters in battle, utilizing effect cards to gain tactical advantages.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Game Mechanics](#game-mechanics)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Agent Types](#agent-types)
- [Project Structure](#project-structure)
- [Advanced Features](#advanced-features)
- [Authors](#authors)

## Overview

This project demonstrates the application of reinforcement learning (RL) algorithms in adversarial game-playing scenarios. The game features:

- **Q-Learning Agent**: Traditional tabular Q-learning approach
- **DQN Agent**: Deep Q-Network using neural networks
- **Rule-Based Agents**: Strategic AI opponents using hard-coded decision trees
- **Interactive Play**: Human vs AI gameplay
- **Tournament System**: Competitive matchups between multiple agents

## Features

### Game Features
- 🎴 **Monster Combat System**: Deploy one of three unique monsters per round
- ⚡ **Effect Cards**: Cast powerful abilities with energy management mechanics
- 🛡️ **Buff System**: Apply temporary stat modifications with duration tracking
- 📊 **Three-Round Format**: Best-of-three matches determine the winner
- 💾 **Save/Load System**: Persist trained agent progress

### AI Features
- 🤖 **Multiple Learning Algorithms**: Q-Learning and Deep Q-Networks
- 🎯 **Strategy Adaptation**: Agents learn optimal action selection
- 📈 **Training Framework**: Efficient episode-based training system
- 🏆 **Tournament Mode**: Round-robin tournaments with leaderboards

### Interactive Features
- 🎮 **Interactive CLI Menu**: Intuitive terminal-based user interface
- 📊 **Real-time Statistics**: Track agent performance and win rates
- 🎨 **Colored Output**: Enhanced readability with ANSI color codes

## Game Mechanics

### Core Concepts

**Monsters**
- Each monster has three base stats: HP, Attack, and Defense
- Damage calculation: `actual_damage = max(0, attack - defense)`
- Monsters have temporary buff effects that modify attack and defense

**Energy System**
- Each player starts with 10 energy per round
- Energy regenerates by 3 points per turn
- Effect cards consume energy to activate

**Effect Cards**
- 15 unique effect cards with various properties:
  - **Damage Effects**: Direct damage to opponent's active monster
  - **Healing Effects**: Restore HP to player's active monster
  - **Buff Effects**: Temporarily increase attack or defense (2-3 turns)
  - **Mixed Effects**: Combination of damage and healing/buffs

**Round Structure**
1. Monster Selection Phase: Each player chooses their starting monster
2. Battle Phase: Players alternate turns, choosing actions:
   - Pass (no action)
   - Use Effect Card (if energy allows)
   - Switch Active Monster
3. Round concludes when one team has no living monsters
4. Three rounds determine the match winner (best-of-three)

### Monster Roster

20 unique monsters with varied stat distributions:
- **Balanced**: Fire Dragon, Ice Wolf
- **Aggressive**: Shadow Assassin, Dark Reaper (high attack, low defense)
- **Defensive**: Earth Golem, Mountain Giant (high HP/defense, low attack)
- **Specialized**: Nature Treant, Holy Paladin (mixed specializations)

## Installation

### Requirements
- Python 3.7+
- NumPy
- PyTorch (for DQN agent)

### Setup

1. Clone or download the project:
```bash
cd Card_game_using_RL
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or manually install required packages:
```bash
pip install numpy torch
```

3. *(Optional)* Verify the installation:
```bash
python main.py
```

## Quick Start

### Run the Game

```bash
python main.py
```

This launches the interactive menu with the following options:

```
=== Play ===
1. Play Game (vs Current AI)
2. Quick Play (vs Random Bot)

=== Training ===
3. Train Q-Learning Agent
4. Train DQN Agent
5. Quick Train (100 episodes)
6. Extended Train (1000 episodes)

=== Agent Management ===
7. Load Agent
8. Save Current Agent
9. Create New Agent

=== Tournament ===
10. Run Tournament (All Bots)
11. Custom Tournament

12. Exit
```

### Basic Gameplay Example

1. Select **Option 2: Quick Play** to face a random rule-based opponent
2. Choose your starting monster from the three available options
3. Each turn, decide whether to:
   - Pass (skip your action)
   - Use an effect card (if you have energy)
   - Switch to a different monster
4. Defeat all opponent monsters to win the round
5. Win 2 out of 3 rounds to win the match

## Usage

### Training an Agent

#### Train Q-Learning Agent (100 episodes)
```
Menu Option 5 → Select "1" for Q-Learning Agent
```

#### Train DQN Agent (1000 episodes)
```
Menu Option 6 → Select "2" for DQN Agent
```

#### Custom Training via Python Script

```python
from game_engine import MonsterCardGame
from agents import QLearningAgent, DefensiveAgent
from training import train_agent

# Create agent
agent = QLearningAgent(learning_rate=0.1, epsilon=0.3)

# Train against defensive bot
opponent = DefensiveAgent()
trained_agent = train_agent(
    agent, 
    episodes=500, 
    opponent=opponent, 
    save_path="my_agent.pkl",
    verbose=True
)
```

### Running a Tournament

#### Full Tournament (All Available Agents)
```
Menu Option 10
```

This will run round-robin matches between:
- Q-Learning Agent
- DQN Agent
- Aggressive Bot
- Defensive Bot
- Balanced Bot

#### Custom Tournament
```
Menu Option 11
```

Select which agents you want to include in the tournament and specify games per matchup.

### Playing Against Your Agent

1. Train an agent and save it
2. Load the agent (**Option 7**)
3. Play against it (**Option 1**)

## Agent Types

### Reinforcement Learning Agents

#### Q-Learning Agent
- **Algorithm**: Tabular Q-learning with epsilon-greedy exploration
- **State Representation**: Discretized game state vector (23 dimensions)
- **Features**:
  - Fast convergence on small state spaces
  - Minimal memory for small games
  - Exploration decay based on game round
  
**Parameters**:
```python
learning_rate = 0.1      # Q-update step size
discount_factor = 0.95   # Future reward weight
epsilon = 0.3           # Initial exploration rate
```

#### DQN Agent (Deep Q-Network)
- **Algorithm**: Deep Q-Network with experience replay
- **Architecture**: 4-layer neural network (128 hidden units)
- **Features**:
  - Handles larger state spaces
  - Target network for stability
  - Experience replay buffer (10,000 capacity)
  - Batch learning (64 samples)

**Parameters**:
```python
state_size = 23          # State vector dimensions
action_size = 7          # Possible actions
learning_rate = 0.001    # Adam optimizer learning rate
epsilon_decay = 0.995    # Exploration decay per episode
```

### Rule-Based Agents

#### Aggressive Agent
- **Strategy**: Maximize damage output
- **Priority**: Uses highest damage effect cards
- **Monster Selection**: Chooses highest attack monster
- **Use Case**: Training aggressive counter-strategies

#### Defensive Agent
- **Strategy**: Minimize damage taken
- **Priority**: Heals when HP is low, uses defensive buffs
- **Monster Selection**: Switches to healthiest monster when needed
- **Use Case**: Training sustainable strategies

#### Balanced Agent
- **Strategy**: Dynamic decision-making
- **Priority**: Adapts action selection based on current game state
- **Features**: Considers both offense and defense
- **Use Case**: Realistic opponent training

## Project Structure

```
Card_game_using_RL/
├── README.md                 # This file
├── requirements.txt          # Project dependencies
├── main.py                   # Interactive game menu and entry point
├── game_engine.py            # Core game logic and state management
├── cards.py                  # Monster and EffectCard classes
├── agents.py                 # RL and rule-based agent implementations
├── training.py               # Training loop and utilities
├── tournament.py             # Tournament system and scoring
├── game_data.py              # Monster and effect deck definitions
├── colors.py                 # Terminal color utilities
└── __init__.py               # Package initialization
```

### File Descriptions

| File | Purpose |
|------|---------|
| `game_engine.py` | Manages game state, turn logic, action resolution, and win conditions |
| `cards.py` | Defines Monster and Effect card classes with buff system |
| `agents.py` | Implements Q-Learning, DQN, and rule-based agents |
| `training.py` | Provides `play_training_game()` and `train_agent()` functions |
| `tournament.py` | Tournament management, matchup scheduling, and results tracking |
| `game_data.py` | Monster roster (20 unique cards) and effect deck (15 cards) |
| `main.py` | CLI menu system and interactive gameplay loop |
| `colors.py` | ANSI color codes for enhanced terminal output |

## Advanced Features

### State Representation

The game state is represented as a 23-dimensional vector:
```
[
  player_active_hp, player_active_attack, player_active_defense,
  player_monster2_hp, player_monster3_hp,
  opponent_active_hp, opponent_active_attack, opponent_active_defense,
  opponent_monster2_hp, opponent_monster3_hp,
  player_energy, opponent_energy,
  player_buffs_count, opponent_buffs_count,
  effect_card_1_type, effect_card_1_cost,
  effect_card_2_type, effect_card_2_cost,
  effect_card_3_type, effect_card_3_cost,
  round_number, turn_count
]
```

### Reward Shaping

Agents receive rewards for:
- **Step rewards**: +0.1 for successful actions
- **Round win**: +100 for winning a round
- **Round loss**: -100 for losing a round

### Buff System

Buffs have:
- **Duration**: Number of turns the buff remains active
- **Effect**: Temporary modifications to Attack/Defense stats
- **Owner**: Buffs only tick down on the owner's turn
- **Stack**: Multiple buffs can be active simultaneously

## Performance Metrics

### Tracking Statistics

Agents track:
- `games_played`: Total matches completed
- `rounds_won`: Individual rounds won across all games
- `rounds_lost`: Individual rounds lost across all games

### Win Rate Calculation

```
win_rate = (games_won / total_games) × 100%
```

## Tips for Training

### Q-Learning Agent
- Best for learning basic strategies
- Converges quickly (100-200 episodes)
- Good baseline agent
- Deterministic decisions after training

### DQN Agent
- Requires more episodes for convergence (500+)
- Better generalization to unseen states
- More computationally intensive
- Smoother decision-making

### Training Against Different Opponents

1. **Aggressive Bot**: Learn defensive strategies
2. **Defensive Bot**: Learn to break through defenses
3. **Balanced Bot**: Learn adaptive strategies
4. **Mixed Opponents**: General-purpose strategy

## Troubleshooting

### Common Issues

**Q: "Module not found" errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Q: DQN agent training is slow**
- This is normal - neural network training requires more computation
- Use GPU if available: PyTorch will auto-detect CUDA

**Q: Agent not improving**
- Increase training episodes
- Try different hyperparameters (learning rate, epsilon)
- Train against different opponent types

**Q: Out of memory errors**
- Reduce batch size in DQNAgent
- Reduce experience replay buffer size
- Close other applications

## Future Enhancements

Potential improvements for the project:

- Policy Gradient methods (A3C, PPO)
- Multi-agent learning scenarios
- Extended card pool and monster roster
- Graphical UI (Pygame/Tkinter)
- Web-based interface
- Saved game replays
- Advanced metrics and analytics
- Curriculum learning

## Contributing

To extend this project:

1. Add new effect cards in `game_data.py`
2. Implement new agent types in `agents.py`
3. Extend game mechanics in `game_engine.py`
4. Add new interactive features in `main.py`

## Authors

This project was built by:

- **Shiv** ([@Chandel247](https://github.com/Chandel247)): Game design, game mechanics, the DQN agent, and the rule-based agents (Aggressive, Defensive, Balanced)
- **Saksham** ([@saksham23csu274](https://github.com/saksham23csu274)): The interactive CLI and the Q-Learning agent

## License

This project is provided as-is for educational purposes.

## Acknowledgments

This project demonstrates practical applications of:
- Reinforcement Learning (Q-Learning, Deep Q-Networks)
- Game AI development
- Neural network training with PyTorch
- Python software architecture

---

**For questions or improvements, feel free to extend and customize this project!**
