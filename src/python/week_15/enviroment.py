import player
import random
import numpy as np
from typing import Tuple, Optional

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class enviroment:
    def __init__(self, grid):
        self.GRID = self.place_rewards(grid)
        self.START = self.find_position(grid, 2)
        self.FINSIH = self.find_position(grid, 3)
    
    # Positie vinden
    # 2 = start
    # 3 = finish
    def find_position(self, grid, id):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == id:
                    return (x, y)
        
        return (0, 0)

    # Op alle vakken een reward plaatsen
    # Muren: -100
    # Paden: -1
    # Finish: 100
    def place_rewards(self, grid):
        rewards = [[0 for x in range(len(grid[0]))] for y in range(len(grid))]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    rewards[y][x] = -1
                elif grid[y][x] == 1:
                    rewards[y][x] = -100
                elif grid[y][x] == 2:
                    rewards[y][x] = -1
                elif grid[y][x] == 3:
                    rewards[y][x] = 100
        
        for y in rewards:
            print(y)
        
        return rewards