# main.py
from engine import GameEngine
from players import RandomAIPlayer, GreedyAIPlayer, StrategicAIPlayer
from ui import TerminalUI

def main():
    ui = TerminalUI()
    
    while True:
        choice = ui.display_menu()
        
        if choice == '1':
            opponent = RandomAIPlayer("Computer (Random)", "O")
        elif choice == '2':
            opponent = GreedyAIPlayer("Computer (Greedy)", "O")
        elif choice == '3':
            opponent = StrategicAIPlayer("Computer (Strategic)", "O")
        elif choice == '4':
            ui.print_message("Thanks for playing!")
            break
        else:
            ui.prompt_invalid_choice()
            continue
            
        # Pass both the opponent and the shared UI into the engine
        game = GameEngine(opponent, ui)
        game.play()
        
        replay = ui.prompt_replay()
        if replay != 'y':
            ui.print_message("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
