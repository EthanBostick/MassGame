# players.py
import random

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.mass = 10
        self.passive_income = 2
        self.multiplier = 1.0 

    def apply_passive_income(self):
        self.mass += self.passive_income

    def get_valid_actions(self):
        actions = ["1"] 
        if self.mass >= 15: actions.append("2") 
        actions.append("3") 
        if self.mass >= 20: actions.append("4") 
        return actions

    def execute_action(self, choice, opponent):
        mult = self.multiplier
        self.multiplier = 1.0 
        
        action_text = ""

        if choice == "1":
            gain = int(12 * mult)
            self.mass += gain
            action_text = f"foraged for {gain} mass."
        elif choice == "2":
            self.mass -= 15
            gain = int(4 * mult)
            self.passive_income += gain
            action_text = f"invested 15 mass to gain +{gain} passive income."
        elif choice == "3":
            self.multiplier = 2.0
            action_text = "overcharged! Their next action is 2x stronger."
        elif choice == "4":
            self.mass -= 20
            damage = int(25 * mult)
            opponent.mass = max(0, opponent.mass - damage) 
            action_text = f"sabotaged {opponent.name} for {damage} mass!"

        return f"{self.name} {action_text}"


class HumanPlayer(Player):
    def act(self, opponent, ui):
        valid_actions = self.get_valid_actions()
        # We delegate the prompt loop entirely to our UI interface
        choice = ui.prompt_human_action(valid_actions)
        return self.execute_action(choice, opponent)


class RandomAIPlayer(Player):
    def act(self, opponent, ui=None):
        valid_actions = self.get_valid_actions()
        choice = random.choice(valid_actions)
        return self.execute_action(choice, opponent)

class GreedyAIPlayer(Player):
    def act(self, opponent, ui=None):
        return self.execute_action("1", opponent)

class StrategicAIPlayer(Player):
    def act(self, opponent, ui=None):
        valid_actions = self.get_valid_actions()
        total_board_mass = self.mass + opponent.mass
        
        if "2" in valid_actions and total_board_mass < 200:
            return self.execute_action("2", opponent)
        if "4" in valid_actions and opponent.passive_income > self.passive_income:
            return self.execute_action("4", opponent)
        if "3" in valid_actions and self.multiplier == 1.0:
            return self.execute_action("3", opponent)
            
        return self.execute_action("1", opponent)
