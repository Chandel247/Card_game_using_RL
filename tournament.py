from typing import List, Dict
from game_engine import MonsterCardGame
from agents import QLearningAgent, DQNAgent, AggressiveAgent, DefensiveAgent, BalancedAgent
from training import play_training_game
from colors import Colors

class Tournament:
    """Run round-robin tournament between multiple agents"""
    
    def __init__(self, agents: List, games_per_matchup: int = 5):
        self.agents = agents
        self.games_per_matchup = games_per_matchup
        self.results: Dict[str, Dict[str, int]] = {}
        
        for agent in agents:
            self.results[agent.name] = {
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'points': 0
            }
    
    def run_tournament(self, verbose: bool = True):
        """Run full round-robin tournament"""
        if verbose:
            print(Colors.header_color("\n" + "=" * 60))
            print(Colors.header_color("TOURNAMENT START"))
            print(Colors.header_color("=" * 60))
            print(f"Participants: {len(self.agents)} agents")
            print(f"Games per matchup: {self.games_per_matchup}")
            print()
        
        matchup_count = 0
        total_matchups = len(self.agents) * (len(self.agents) - 1) // 2
        
        for i, agent1 in enumerate(self.agents):
            for agent2 in self.agents[i+1:]:
                matchup_count += 1
                
                if verbose:
                    print(Colors.header_color(f"\nMatchup {matchup_count}/{total_matchups}: ") +
                          f"{Colors.player_color(agent1.name)} vs {Colors.opponent_color(agent2.name)}")
                
                agent1_wins = 0
                agent2_wins = 0
                draws = 0
                
                for game_num in range(self.games_per_matchup):
                    game = MonsterCardGame()
                    result = play_training_game(agent1, agent2, game, verbose=False)
                    
                    if result == 0:
                        agent1_wins += 1
                        self.results[agent1.name]['wins'] += 1
                        self.results[agent2.name]['losses'] += 1
                        self.results[agent1.name]['points'] += 3
                    elif result == 1:
                        agent2_wins += 1
                        self.results[agent2.name]['wins'] += 1
                        self.results[agent1.name]['losses'] += 1
                        self.results[agent2.name]['points'] += 3
                    else:
                        draws += 1
                        self.results[agent1.name]['draws'] += 1
                        self.results[agent2.name]['draws'] += 1
                        self.results[agent1.name]['points'] += 1
                        self.results[agent2.name]['points'] += 1
                
                if verbose:
                    print(f"  Results: {Colors.player_color(f'{agent1.name}: {agent1_wins}')} | "
                          f"{Colors.opponent_color(f'{agent2.name}: {agent2_wins}')} | "
                          f"Draws: {draws}")
        
        if verbose:
            self.print_standings()
    
    def print_standings(self):
        """Print tournament standings"""
        print(Colors.header_color("\n" + "=" * 60))
        print(Colors.header_color("FINAL STANDINGS"))
        print(Colors.header_color("=" * 60))
        
        # Sort by points
        sorted_agents = sorted(self.results.items(), 
                             key=lambda x: x[1]['points'], 
                             reverse=True)
        
        print(f"{'Rank':<6} {'Agent':<20} {'Wins':<6} {'Losses':<8} {'Draws':<6} {'Points':<8}")
        print("-" * 60)
        
        for rank, (agent_name, stats) in enumerate(sorted_agents, 1):
            color_func = Colors.success_color if rank == 1 else (
                Colors.player_color if rank <= 3 else lambda x: x
            )
            
            print(f"{rank:<6} {color_func(agent_name):<30} "
                  f"{stats['wins']:<6} {stats['losses']:<8} "
                  f"{stats['draws']:<6} {stats['points']:<8}")
        
        print("=" * 60)
        
        champion = sorted_agents[0][0]
        print(Colors.success_color(f"\n🏆 Champion: {champion}! 🏆\n"))
