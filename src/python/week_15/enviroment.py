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

# ACTIONS = {
#     "UP": (-1, 0),
#     "DOWN": (1, 0),
#     "LEFT": (0, -1),
#     "RIGHT": (0, 1)
# }

class enviroment:
    def __init__(self, grid, plr : player.player):
        # GRID
        self.GRID = grid
        self.GRID_HEIGHT = len(grid)
        self.GRID_WIDTH = len(grid[0])
        
        # AGENT POSITION
        self.x, self.y = plr.get_player_position()
        
        # ACTIONS
        self.steps = 0
        
        # STATES
        self.allowed_states = None
        self.construct_allowed_sates()
    
    def movement_check(self, state, action):
        y, x = state
        dx, dy = ACTIONS[action]
        new_x = x + dx
        new_y = y + dy

        if new_x < 0 or new_x >= self.GRID_WIDTH or new_y < 0 or new_y >= self.GRID_HEIGHT:
            return False

        return self.GRID[new_y][new_x] in (0, 2, 3)

    
    def construct_allowed_sates(self):
        allowed_states = {}
        
        for y, row in enumerate(self.GRID):
            for x, col in enumerate(row):
                if self.GRID[y][x] != 1:
                    allowed_states[(y, x)] = []
                    for action in ACTIONS:
                        if self.movement_check((y, x), action):
                            allowed_states[(y, x)].append(action)
        
        self.allowed_states = allowed_states
    
    def update(self, action):
        y, x = self.y, self.x
        self.GRID[y][x] = 0
        y += ACTIONS[action][1]
        x += ACTIONS[action][0]
        
        self.y, self.x = y, x
        self.GRID[y][x] = 2
        self.steps += 1
    
    def is_game_over(self):
        return self.GRID[self.y][self.x] == 3
    
    def give_reward(self):
        if self.GRID[self.y][self.x] == 3:
            return 0
        return -1

    def get_state_and_reward(self):
        return (self.y, self.x), self.give_reward()
    
    
        