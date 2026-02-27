# board.py
class Board:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.total_cells = width * height
