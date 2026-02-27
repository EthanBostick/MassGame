# ui.py
import os
from config import GREEN, RED, RESET

class TerminalUI:
    def __init__(self):
        # We will cache the turn state here so the UI can refresh itself!
        self._current_state = {}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear_screen()
        print("========================")
        print("    MASS DUEL V1.0      ")
        print("========================")
        print("Choose your opponent:")
        print("1. Random AI (Easy)")
        print("2. Greedy AI (Easy)")
        print("3. Strategic AI (Hard)")
        print("4. Quit")
        return input("\nEnter choice (1-4): ").strip()

    def prompt_invalid_choice(self):
        input("Invalid choice. Press Enter to try again.")

    def prompt_replay(self):
        return input("\nWould you like to play again? (y/n): ").strip().lower()

    def print_message(self, message):
        print(message)

    # Replaces display_turn_header. It now takes all the info needed to render the whole screen.
    def display_game_state(self, board, turn, p1, p2, log1, log2, error_msg=""):
        # Save the state in case we need to redraw due to a typo
        self._current_state = {
            'board': board, 'turn': turn, 'p1': p1, 'p2': p2,
            'log1': log1, 'log2': log2
        }
        
        self.clear_screen()
        print(f"--- TURN {turn} ---")
        print(f"{p1.name} (X) | Mass: {p1.mass} | Passive: +{p1.passive_income}/turn | Mult: {p1.multiplier}x")
        print(f"{p2.name} (O) | Mass: {p2.mass} | Passive: +{p2.passive_income}/turn | Mult: {p2.multiplier}x")
        print("-" * 25)
        print(f"Log: {log1}")
        print(f"Log: {log2}")
        
        self.render_board(board, p1, p2)
        
        # Print the error message in red if one exists
        if error_msg:
            print(f"\n{RED}{error_msg}{RESET}")

    def prompt_human_action(self, valid_actions):
        error_msg = ""
        while True:
            if error_msg:
                # Unpack the cached state and pass the error message to trigger a full screen refresh!
                self.display_game_state(**self._current_state, error_msg=error_msg)
                
            print("\nActions: [1] Forage (+12 Mass) | [2] Invest (Cost: 15, +4 Passive) | [3] Overcharge (2x Next Turn) | [4] Sabotage (Cost: 20, -25 Enemy Mass)")
            choice = input("Choose your action (1-4): ").strip()
            if choice in valid_actions:
                return choice
            
            # If we get here, the input was bad. Set the error message for the next loop iteration.
            error_msg = "Invalid choice or not enough mass. Try again."

    def render_board(self, board, player1, player2):
        p1_cells = min(player1.mass, board.total_cells)
        p2_cells = min(player2.mass, board.total_cells - p1_cells)
        empty_cells = max(0, board.total_cells - (p1_cells + p2_cells))

        p1_colored = f"{GREEN}{player1.symbol}{RESET}"
        p2_colored = f"{RED}{player2.symbol}{RESET}"

        board_array = [p1_colored] * p1_cells + ["."] * empty_cells + [p2_colored] * p2_cells

        print("\n+" + "-" * (board.width * 2 + 1) + "+")
        for row in range(board.height):
            start_idx = row * board.width
            end_idx = start_idx + board.width
            row_chars = board_array[start_idx:end_idx]
            print("| " + " ".join(row_chars) + " |")
        print("+" + "-" * (board.width * 2 + 1) + "+")

    def display_game_over(self, p1, p2):
        print("\n--- GAME OVER ---")
        if p1.mass > p2.mass:
            print("You have overtaken the board! YOU WIN!")
        elif p2.mass > p1.mass:
            print("The computer has overtaken the board! YOU LOSE!")
        else:
            print("It's a perfect tie!")
