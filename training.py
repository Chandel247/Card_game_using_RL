import random
from typing import Optional
from game_engine import MonsterCardGame
from agents import QLearningAgent, DQNAgent, AggressiveAgent, DefensiveAgent, BalancedAgent
from colors import Colors

def play_training_game(agent1, agent2, game: MonsterCardGame, verbose: bool = False) -> int:
    """
    Play a training game between two agents.
    Returns 0 if agent1 wins, 1 if agent2 wins, -1 for draw
    """
    round_results = []
    
    for round_num in range(1, 4):
        if not game.start_new_round():
            break
        
        # Auto-select starting monsters
        if hasattr(agent1, 'choose_action'):
            agent1_choice = max(range(3), key=lambda i: game.player_monsters[i].hp)
        else:
            agent1_choice = random.randint(0, 2)
        game.select_starting_monster(0, agent1_choice)
        
        if hasattr(agent2, 'choose_action'):
            agent2_choice = max(range(3), key=lambda i: game.opponent_monsters[i].hp)
        else:
            agent2_choice = random.randint(0, 2)
        game.select_starting_monster(1, agent2_choice)
        
        game.draw_effects()
        
        turn_count = 0
        max_turns = 100
        
        while not game.is_round_over() and turn_count < max_turns:
            current_player = game.current_player
            
            if current_player == 0:
                state_before = game.get_state_vector(0)
                action = agent1.choose_action(game, 0, round_num)
                msg, turn_ended = game.step(0, action)
                
                if hasattr(agent1, 'update'):
                    reward = 0.1 if not turn_ended else 0
                    if game.is_round_over():
                        reward = 100 if game.get_round_winner() == 0 else -100
                    state_after = game.get_state_vector(0)
                    agent1.update(state_before, action, reward, state_after, game.is_round_over())
                
                if not turn_ended:
                    continue
            else:
                state_before = game.get_state_vector(1)
                action = agent2.choose_action(game, 1, round_num)
                msg, turn_ended = game.step(1, action)
                
                if hasattr(agent2, 'update'):
                    reward = 0.1 if not turn_ended else 0
                    if game.is_round_over():
                        reward = 100 if game.get_round_winner() == 1 else -100
                    state_after = game.get_state_vector(1)
                    agent2.update(state_before, action, reward, state_after, game.is_round_over())
                
                if not turn_ended:
                    continue
            
            turn_count += 1
            
            if not game.is_round_over():
                buff_msgs = game.next_turn()
        
        winner = game.get_round_winner()
        round_results.append(winner)
        
        if verbose:
            winner_name = agent1.name if winner == 0 else (agent2.name if winner == 1 else "Draw")
            print(f"  Round {round_num}: {Colors.success_color(winner_name)}")
    
    # Determine game winner
    agent1_wins = sum(1 for r in round_results if r == 0)
    agent2_wins = sum(1 for r in round_results if r == 1)
    
    if agent1_wins > agent2_wins:
        return 0
    elif agent2_wins > agent1_wins:
        return 1
    else:
        return -1

def train_agent(agent, episodes: int = 500, opponent=None, 
                save_path: Optional[str] = None, verbose: bool = True):
    """Train an agent against various opponents"""
    
    if opponent is None:
        opponents = [AggressiveAgent(), DefensiveAgent(), BalancedAgent()]
    else:
        opponents = [opponent]
    
    wins = 0
    losses = 0
    draws = 0
    
    print(Colors.header_color(f"\nTraining {agent.name} for {episodes} episodes..."))
    print("=" * 60)
    
    for episode in range(episodes):
        game = MonsterCardGame()
        opponent = random.choice(opponents)
        
        result = play_training_game(agent, opponent, game, verbose=False)
        
        if result == 0:
            wins += 1
            agent.rounds_won += 1
        elif result == 1:
            losses += 1
            agent.rounds_lost += 1
        else:
            draws += 1
        
        agent.games_played += 1
        
        if verbose and (episode + 1) % 100 == 0:
            win_rate = wins / (episode + 1) * 100
            print(f"Episode {episode + 1}/{episodes} | "
                  f"Win Rate: {Colors.success_color(f'{win_rate:.1f}%')} | "
                  f"W:{wins} L:{losses} D:{draws}")
    
    print("=" * 60)
    print(Colors.success_color("Training complete!"))
    print(f"Final Win Rate: {Colors.success_color(f'{wins / episodes * 100:.1f}%')}")
    print(f"W:{Colors.success_color(str(wins))} "
          f"L:{Colors.error_color(str(losses))} "
          f"D:{Colors.warning_color(str(draws))}")
    
    if save_path:
        agent.save(save_path)
    
    return agent
