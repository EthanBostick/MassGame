# engine.py
from board import Board
from players import HumanPlayer

class GameEngine:
	def __init__(self, opponent, ui):
		self.board = Board(40, 20)
		self.p1 = HumanPlayer("Player", "X")
		self.p2 = opponent
		self.turn = 1
		self.ui = ui

	def play(self):
		last_action_p1 = "Game started."
		last_action_p2 = "Opponent is ready."

		while True:
			
			# 1. Passive Income Phase
			# Apply this FIRST so the player's mass is accurate for their decision
			self.p1.apply_passive_income()
			self.p2.apply_passive_income()
			if (self.p1.mass + self.p2.mass) >= self.board.total_cells:
				break

			# 2. Render Phase
			# Now we cache and draw the state AFTER passive income is added
			self.ui.display_game_state(
				self.board, self.turn, self.p1, self.p2, 
				last_action_p1, last_action_p2
			)

			# 3. Action Phase
			last_action_p1 = self.p1.act(self.p2, self.ui)
			if self.p1.mass + self.p2.mass >= self.board.total_cells:
				break
			last_action_p2 = self.p2.act(self.p1, self.ui)
			if self.p1.mass + self.p2.mass >= self.board.total_cells:
				break

			
			self.turn += 1

		self.ui.clear_screen()
		self.ui.render_board(self.board, self.p1, self.p2)
		self.ui.display_game_over(self.p1, self.p2)
