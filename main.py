import os
from game_engine import MonsterCardGame
from agents import QLearningAgent, DQNAgent, AggressiveAgent, DefensiveAgent, BalancedAgent
from training import train_agent
from tournament import Tournament
from colors import Colors

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game(agent, player_name: str = "Player"):
    """Main game loop"""
    game = MonsterCardGame()
    
    player_wins = 0
    opponent_wins = 0
    
    print(Colors.header_color("=" * 60))
    print(Colors.header_color("MONSTER CARD GAME"))
    print(Colors.header_color("=" * 60))
    print(f"{Colors.player_color(player_name)} vs {Colors.opponent_color(agent.name)}\n")
    
    for round_num in range(1, 4):
        print(f"\n{Colors.header_color('=' * 60)}")
        print(Colors.header_color(f"ROUND {round_num}/3"))
        print(Colors.header_color('=' * 60))
        
        if not game.start_new_round():
            print(Colors.error_color("Not enough cards for a new round!"))
            break
        
        # Monster selection phase
        print(Colors.player_color("\nYour monsters:"))
        for i, monster in enumerate(game.player_monsters):
            print(f"  {i}: {monster}")
        
        while game.player_active is None:
            try:
                choice = int(input(Colors.player_color("\nChoose your starting monster (0-2): ")))
                if 0 <= choice <= 2:
                    game.select_starting_monster(0, choice)
                else:
                    print(Colors.error_color("Invalid choice!"))
            except ValueError:
                print(Colors.error_color("Please enter a number!"))
        
        # AI selects monster
        ai_choice = max(range(3), key=lambda i: game.opponent_monsters[i].hp)
        game.select_starting_monster(1, ai_choice)
        print(Colors.opponent_color(f"\n{agent.name} chose: {game.opponent_monsters[ai_choice].name}"))
        
        # Battle phase
        game.draw_effects()
        
        while not game.is_round_over():
            current_player = game.current_player
            
            if current_player == 0:  # Human player
                print(Colors.header_color(f"\n--- Your Turn (Round {round_num}) ---"))
                print(f"Energy: {Colors.color_text(f'{game.player_energy}/{game.max_energy}', Colors.CYAN)}")
                print(f"Your active: {game.player_monsters[game.player_active]}")
                print(f"Opponent's active: {game.opponent_monsters[game.opponent_active]}")
                
                print(Colors.effect_color("\nAvailable effects:"))
                for i, effect in enumerate(game.available_effects):
                    print(f"  {i+1}: {effect}")
                
                print(Colors.player_color("\nYour monsters:"))
                for i, m in enumerate(game.player_monsters):
                    status = Colors.success_color("ACTIVE") if i == game.player_active else (
                        Colors.warning_color("ALIVE") if m.is_alive() else Colors.error_color("DEAD")
                    )
                    print(f"  {i}: {m} [{status}]")
                
                legal = game.get_legal_actions(0)
                print(f"\n{Colors.BRIGHT_BLACK}Actions: 0=Pass/Attack, 1-3=Use Effect, 4-6=Switch Monster{Colors.RESET}")
                print(f"Legal actions: {Colors.success_color(str(legal))}")
                
                while True:
                    try:
                        action = int(input(Colors.player_color("\nYour action: ")))
                        if action in legal:
                            state = game.get_state_vector(0)
                            msg, turn_ended = game.step(0, action)
                            print(f"\n{msg}")
                            
                            if hasattr(agent, 'learn_from_player'):
                                agent.learn_from_player(action, state)
                            
                            if turn_ended:
                                break
                        else:
                            print(Colors.error_color("Illegal action!"))
                    except ValueError:
                        print(Colors.error_color("Please enter a number!"))
            
            else:  # AI opponent
                print(Colors.header_color(f"\n--- {agent.name}'s Turn ---"))
                state_before = game.get_state_vector(1)
                
                action = agent.choose_action(game, 1, round_num)
                msg, turn_ended = game.step(1, action)
                print(f"{msg}")
                
                if hasattr(agent, 'update'):
                    reward = 0
                    if game.is_round_over():
                        reward = 100 if game.get_round_winner() == 1 else -100
                    
                    state_after = game.get_state_vector(1)
                    agent.update(state_before, action, reward, state_after, game.is_round_over())
                
                if not turn_ended:
                    continue
            
            if not game.is_round_over():
                buff_msgs = game.next_turn()
                if buff_msgs:
                    for msg in buff_msgs:
                        print(Colors.warning_color(f"  {msg}"))
        
        # Round results
        winner = game.get_round_winner()
        if winner == 0:
            print(Colors.success_color(f"\n🎉 You won Round {round_num}!"))
            player_wins += 1
        else:
            print(Colors.error_color(f"\n💀 {agent.name} won Round {round_num}!"))
            opponent_wins += 1
            agent.rounds_won += 1
        
        print(Colors.warning_color(f"\nScore: {player_name} {player_wins} - {opponent_wins} {agent.name}"))
        input(Colors.BRIGHT_BLACK + "\nPress Enter to continue..." + Colors.RESET)
    
    # Final results
    print(Colors.header_color(f"\n{'=' * 60}"))
    print(Colors.header_color("GAME OVER"))
    print(Colors.header_color('=' * 60))
    print(f"{player_name}'s wins: {Colors.success_color(str(player_wins))}")
    print(f"{agent.name}'s wins: {Colors.error_color(str(opponent_wins))}")
    
    if player_wins > opponent_wins:
        print(Colors.success_color("\n🏆 You are the CHAMPION! 🏆"))
    elif opponent_wins > player_wins:
        print(Colors.error_color(f"\n💀 {agent.name} has defeated you! 💀"))
    else:
        print(Colors.warning_color("\n🤝 It's a TIE! 🤝"))
    
    agent.games_played += 1

def main_menu():
    """Main menu system"""
    agent = None
    agent_loaded = False
    
    while True:
        clear_screen()
        print(Colors.header_color("=" * 60))
        print(Colors.header_color("MONSTER CARD GAME - MAIN MENU"))
        print(Colors.header_color("=" * 60))
        
        if agent_loaded and agent:
            print(f"\n{Colors.success_color('Current Agent:')} {agent.name}")
            print(f"{Colors.BRIGHT_BLACK}Stats: {agent.games_played} games, "
                  f"{agent.rounds_won} rounds won{Colors.RESET}")
        else:
            print(f"\n{Colors.warning_color('No agent loaded')}")
        
        print(f"\n{Colors.CYAN}=== Play ==={Colors.RESET}")
        print("1. Play Game (vs Current AI)")
        print("2. Quick Play (vs Random Bot)")
        
        print(f"\n{Colors.MAGENTA}=== Training ==={Colors.RESET}")
        print("3. Train Q-Learning Agent")
        print("4. Train DQN Agent")
        print("5. Quick Train (100 episodes)")
        print("6. Extended Train (1000 episodes)")
        
        print(f"\n{Colors.YELLOW}=== Agent Management ==={Colors.RESET}")
        print("7. Load Agent")
        print("8. Save Current Agent")
        print("9. Create New Agent")
        
        print(f"\n{Colors.GREEN}=== Tournament ==={Colors.RESET}")
        print("10. Run Tournament (All Bots)")
        print("11. Custom Tournament")
        
        print(f"\n{Colors.RED}12. Exit{Colors.RESET}")
        
        choice = input(Colors.player_color("\nEnter your choice (1-12): ")).strip()
        
        if choice == '1':
            clear_screen()
            if not agent_loaded or agent is None:
                print(Colors.warning_color("No agent loaded. Loading default Balanced Bot..."))
                agent = BalancedAgent()
                agent_loaded = True
                input("Press Enter to continue...")
            play_game(agent)
            input(Colors.BRIGHT_BLACK + "\nPress Enter to return to menu..." + Colors.RESET)
        
        elif choice == '2':
            clear_screen()
            bots = [AggressiveAgent(), DefensiveAgent(), BalancedAgent()]
            bot = random.choice(bots)
            print(Colors.success_color(f"Playing against {bot.name}!"))
            play_game(bot)
            input(Colors.BRIGHT_BLACK + "\nPress Enter to return to menu..." + Colors.RESET)
        
        elif choice == '3':
            clear_screen()
            print(Colors.header_color("Training Q-Learning Agent..."))
            try:
                episodes = int(input("Episodes (default 500): ") or "500")
                save_name = input("Save filename (default: q_agent.pkl): ").strip() or "q_agent.pkl"
                
                agent = QLearningAgent(name="Trained-Q-Agent")
                train_agent(agent, episodes=episodes, save_path=save_name)
                agent_loaded = True
            except ValueError:
                print(Colors.error_color("Invalid input!"))
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            clear_screen()
            print(Colors.header_color("Training DQN Agent..."))
            try:
                episodes = int(input("Episodes (default 500): ") or "500")
                save_name = input("Save filename (default: dqn_agent.pth): ").strip() or "dqn_agent.pth"
                
                agent = DQNAgent(name="Trained-DQN-Agent")
                train_agent(agent, episodes=episodes, save_path=save_name)
                agent_loaded = True
            except ValueError:
                print(Colors.error_color("Invalid input!"))
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            clear_screen()
            agent_type = input("Agent type (1=Q-Learning, 2=DQN): ").strip()
            if agent_type == '1':
                agent = QLearningAgent(name="Quick-Q-Agent")
                train_agent(agent, episodes=100, save_path="quick_q.pkl")
            elif agent_type == '2':
                agent = DQNAgent(name="Quick-DQN-Agent")
                train_agent(agent, episodes=100, save_path="quick_dqn.pth")
            else:
                print(Colors.error_color("Invalid choice!"))
                input("\nPress Enter to continue...")
                continue
            agent_loaded = True
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            clear_screen()
            agent_type = input("Agent type (1=Q-Learning, 2=DQN): ").strip()
            if agent_type == '1':
                agent = QLearningAgent(name="Extended-Q-Agent")
                train_agent(agent, episodes=1000, save_path="extended_q.pkl")
            elif agent_type == '2':
                agent = DQNAgent(name="Extended-DQN-Agent")
                train_agent(agent, episodes=1000, save_path="extended_dqn.pth")
            else:
                print(Colors.error_color("Invalid choice!"))
                input("\nPress Enter to continue...")
                continue
            agent_loaded = True
            input("\nPress Enter to continue...")
        
        elif choice == '7':
            clear_screen()
            print(Colors.header_color("Load Agent"))
            filename = input("Filename: ").strip()
            agent_type = input("Agent type (1=Q-Learning, 2=DQN): ").strip()
            
            if agent_type == '1':
                agent = QLearningAgent()
                if agent.load(filename):
                    agent_loaded = True
            elif agent_type == '2':
                agent = DQNAgent()
                if agent.load(filename):
                    agent_loaded = True
            else:
                print(Colors.error_color("Invalid choice!"))
            
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            clear_screen()
            if not agent_loaded or agent is None:
                print(Colors.error_color("No agent to save!"))
            else:
                filename = input("Save filename: ").strip()
                if filename:
                    agent.save(filename)
            input("\nPress Enter to continue...")
        
        elif choice == '9':
            clear_screen()
            print(Colors.header_color("Create New Agent"))
            print("1. Q-Learning Agent")
            print("2. DQN Agent")
            print("3. Aggressive Bot")
            print("4. Defensive Bot")
            print("5. Balanced Bot")
            
            agent_choice = input("\nChoice: ").strip()
            name = input("Agent name: ").strip() or "Custom-Agent"
            
            if agent_choice == '1':
                agent = QLearningAgent(name=name)
            elif agent_choice == '2':
                agent = DQNAgent(name=name)
            elif agent_choice == '3':
                agent = AggressiveAgent(name=name)
            elif agent_choice == '4':
                agent = DefensiveAgent(name=name)
            elif agent_choice == '5':
                agent = BalancedAgent(name=name)
            else:
                print(Colors.error_color("Invalid choice!"))
                input("\nPress Enter to continue...")
                continue
            
            agent_loaded = True
            print(Colors.success_color(f"\nCreated {agent.name}!"))
            input("\nPress Enter to continue...")
        
        elif choice == '10':
            clear_screen()
            print(Colors.header_color("Running Tournament with All Bots..."))
            
            agents = [
                AggressiveAgent("Aggressive-Bot"),
                DefensiveAgent("Defensive-Bot"),
                BalancedAgent("Balanced-Bot"),
                QLearningAgent(name="Q-Bot-1"),
                QLearningAgent(name="Q-Bot-2"),
            ]
            
            # Quick train the Q-agents
            print(Colors.warning_color("\nPre-training Q-agents..."))
            for q_agent in [a for a in agents if isinstance(a, QLearningAgent)]:
                train_agent(q_agent, episodes=100, verbose=False)
            
            tournament = Tournament(agents, games_per_matchup=3)
            tournament.run_tournament(verbose=True)
            
            input("\nPress Enter to continue...")
        
        elif choice == '11':
            clear_screen()
            print(Colors.header_color("Custom Tournament"))
            
            print("\nAvailable agents:")
            print("1. Aggressive Bot")
            print("2. Defensive Bot")
            print("3. Balanced Bot")
            print("4. New Q-Learning Agent (will be trained)")
            print("5. New DQN Agent (will be trained)")
            print("6. Load from file")
            
            selected_agents = []
            
            while True:
                choice_str = input(f"\nAdd agent (1-6) or 'done' to start ({len(selected_agents)} selected): ").strip()
                
                if choice_str.lower() == 'done':
                    if len(selected_agents) < 2:
                        print(Colors.error_color("Need at least 2 agents!"))
                        continue
                    break
                
                try:
                    agent_choice = int(choice_str)
                    name = input("Agent name: ").strip() or f"Agent-{len(selected_agents)+1}"
                    
                    if agent_choice == 1:
                        selected_agents.append(AggressiveAgent(name))
                    elif agent_choice == 2:
                        selected_agents.append(DefensiveAgent(name))
                    elif agent_choice == 3:
                        selected_agents.append(BalancedAgent(name))
                    elif agent_choice == 4:
                        q_agent = QLearningAgent(name=name)
                        episodes = int(input("Training episodes (default 100): ") or "100")
                        train_agent(q_agent, episodes=episodes, verbose=False)
                        selected_agents.append(q_agent)
                    elif agent_choice == 5:
                        dqn_agent = DQNAgent(name=name)
                        episodes = int(input("Training episodes (default 100): ") or "100")
                        train_agent(dqn_agent, episodes=episodes, verbose=False)
                        selected_agents.append(dqn_agent)
                    elif agent_choice == 6:
                        filename = input("Filename: ").strip()
                        agent_type = input("Type (1=Q, 2=DQN): ").strip()
                        if agent_type == '1':
                            load_agent = QLearningAgent(name=name)
                            if load_agent.load(filename):
                                selected_agents.append(load_agent)
                        elif agent_type == '2':
                            load_agent = DQNAgent(name=name)
                            if load_agent.load(filename):
                                selected_agents.append(load_agent)
                    
                    print(Colors.success_color(f"Added {name}!"))
                except ValueError:
                    print(Colors.error_color("Invalid input!"))
            
            games = int(input("\nGames per matchup (default 3): ") or "3")
            
            tournament = Tournament(selected_agents, games_per_matchup=games)
            tournament.run_tournament(verbose=True)
            
            input("\nPress Enter to continue...")
        
        elif choice == '12':
            print(Colors.success_color("\nThanks for playing! Goodbye!"))
            break
        
        else:
            print(Colors.error_color("Invalid choice!"))
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    import random
    main_menu()
