import random
import numpy as np

class BoardState():
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._game_board = np.array([[0 for i in range(self._width)] for j in range(self._height)])

    def generate_new_state(self):
        self._game_board = np.array([[random.randint(1,10) for i in range(self._width)] for j in range(self._height)])

    def get_state(self):
        return self._game_board

    def update_state(self, state):
        self._game_board = np.array(state)

    def dead_lock(self):
        """
        Check whether the current board is a dead lock
        """
        return None
    
    def logic_action(first_index, second_index):
        """
        Check whether there is an avaliable path from first_index to second_index
        Avaliable actions: 0 turn, 1 turn or 2 turns
        """
        return None
    
if(__name__ == "__main__"):
    width = 5
    height = 6
    game = BoardState(width, height)
    print(game.get_state())
    print(game.generate_new_state())
    print(game.get_state())