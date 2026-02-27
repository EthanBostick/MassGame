import unittest
from unittest.mock import patch

# Import the classes from our refactored files
from players import Player, HumanPlayer, RandomAIPlayer, GreedyAIPlayer, StrategicAIPlayer
from ui import TerminalUI
from board import Board

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        # This runs before EVERY test to ensure a clean slate
        self.p1 = Player("Player 1", "X")
        self.p2 = Player("Player 2", "O")
        self.ui = TerminalUI()
        self.board = Board(40, 20)

    # ---------------------------------------------------------
    # 1. Boundary Conditions
    # ---------------------------------------------------------
    def test_mass_floor_sabotage(self):
        """Ensure Sabotage does not push opponent mass below zero."""
        self.p1.mass = 20  # Exactly enough to afford Sabotage
        self.p2.mass = 10  # Less than the 25 damage Sabotage deals
        
        self.p1.execute_action("4", self.p2)
        
        self.assertEqual(self.p2.mass, 0, "Opponent mass should stop exactly at 0.")

    def test_action_thresholds(self):
        """Ensure get_valid_actions accurately respects mass costs."""
        # Cost of Invest is 15
        self.p1.mass = 14
        self.assertNotIn("2", self.p1.get_valid_actions())
        self.p1.mass = 15
        self.assertIn("2", self.p1.get_valid_actions())

        # Cost of Sabotage is 20
        self.p1.mass = 19
        self.assertNotIn("4", self.p1.get_valid_actions())
        self.p1.mass = 20
        self.assertIn("4", self.p1.get_valid_actions())

    # ---------------------------------------------------------
    # 2. Invalid Input Handling
    # ---------------------------------------------------------
    @patch('builtins.input', side_effect=['5', 'a', '', '2'])
    @patch('builtins.print') # Mock print so our test console stays clean
    def test_invalid_input_loop(self, mock_print, mock_input):
        """Ensure the UI loops until a valid choice is provided."""
        self.p1.mass = 15  # Can afford 1, 2, and 3
        valid_actions = self.p1.get_valid_actions()
        
        # FIX: Populate the UI's _current_state by simulating the engine's initial render phase
        self.ui.display_game_state(self.board, 1, self.p1, self.p2, "Start", "Start")
        
        # The prompt should reject '5', 'a', and '' before accepting '2'
        choice = self.ui.prompt_human_action(valid_actions)
        
        self.assertEqual(choice, '2')
        self.assertEqual(mock_input.call_count, 4, "It should have prompted exactly 4 times.")
	# ---------------------------------------------------------
    # 3. Win/Loss/Tie Detection
    # ---------------------------------------------------------
    @patch('builtins.print')
    def test_win_loss_tie_detection(self, mock_print):
        """Ensure the correct end-game message prints based on final mass."""
        # Test P1 Win
        self.p1.mass = 500
        self.p2.mass = 300
        self.ui.display_game_over(self.p1, self.p2)
        mock_print.assert_any_call("You have overtaken the board! YOU WIN!")
        
        # Test P2 Win
        self.p1.mass = 300
        self.p2.mass = 500
        self.ui.display_game_over(self.p1, self.p2)
        mock_print.assert_any_call("The computer has overtaken the board! YOU LOSE!")
        
        # Test Tie
        self.p1.mass = 400
        self.p2.mass = 400
        self.ui.display_game_over(self.p1, self.p2)
        mock_print.assert_any_call("It's a perfect tie!")

    # ---------------------------------------------------------
    # 4. AI Behavior Validation
    # ---------------------------------------------------------
    def test_greedy_ai(self):
        """Ensure Greedy AI always picks Forage (Option 1)."""
        ai = GreedyAIPlayer("Greedy", "O")
        ai.mass = 100  # Give it enough mass to afford anything
        action_text = ai.act(self.p1)
        self.assertIn("foraged", action_text)

    def test_strategic_ai_early_game(self):
        """Strategic AI should Invest (Option 2) if board is < 25% full."""
        ai = StrategicAIPlayer("Strat", "O")
        ai.mass = 20
        self.p1.mass = 20  # Total board mass is 40 (well under 200 threshold)
        action_text = ai.act(self.p1)
        self.assertIn("invested", action_text)

    def test_strategic_ai_defense(self):
        """Strategic AI should Sabotage (Option 4) if it's losing the passive income war."""
        ai = StrategicAIPlayer("Strat", "O")
        ai.mass = 200
        self.p1.mass = 200 # Total > 200 bypasses early game phase
        
        self.p1.passive_income = 10
        ai.passive_income = 2 
        
        action_text = ai.act(self.p1)
        self.assertIn("sabotaged", action_text)

    # ---------------------------------------------------------
    # 5. Reproducibility (Handling Randomness)
    # ---------------------------------------------------------
    @patch('random.choice', return_value='3')
    def test_random_ai_mocked(self, mock_random):
        """Ensure Random AI executes whatever random.choice returns."""
        ai = RandomAIPlayer("Rand", "O")
        
        # Even though it's RandomAI, we forced random.choice to return '3' (Overcharge)
        action_text = ai.act(self.p1)
        
        self.assertIn("overcharged", action_text)
        mock_random.assert_called_once()


if __name__ == '__main__':
    unittest.main()
