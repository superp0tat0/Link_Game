import random
import numpy as np

def BFS(G, s, t, randc=3, d=None):
    """
    Return True if there is a valid path from s to t, false otherwise.
    
    direction: 0,1,2,3 means up, down, left, right
    """
    print('-' * (4-randc), s, t, randc, d)
    if randc < 0:
        return False
    if s[0] == t[0] and abs(s[1] - t[1]) == 1:
        return True
    if s[1] == t[1] and abs(s[0] - t[0]) == 1:
        return True
    for direction in (0,1,2,3):
        if direction == 0:
            u = (s[0]-1, s[1])
        elif direction == 1:
            u = (s[0]+1, s[1])
        elif direction == 2:
            u = (s[0], s[1]-1)
        else:
            u = (s[0], s[1]+1)
        print('-' * (5-randc), 'try', direction, u, G.shape)
        if 0 <= u[0] < G.shape[1] and 0 <= u[1] < G.shape[0] and G[u[1], u[0]] == 0:
            new_randc = randc if direction == d else randc - 1
            if BFS(G, u, t, new_randc, direction):
                return True

    return False

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