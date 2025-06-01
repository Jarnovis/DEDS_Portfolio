import pygame

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (1, 0),
    "LEFT": (-1, 0),
    "RIGHT": (0, 1)
}

class player:
    def __init__(self, grid):
        self.grid = grid
        self.x, self.y = self.get_start_position()
        
        self.get_start_position()
    
    def get_start_position(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 2:
                    return (x, y)
        
        return (0, 0)
    
    def movement_logic(self, x, y):
        if (0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)):
            if self.grid[y][x] in (0, 2, 3):
                self.x = x
                self.y = y
        
        print(self.x, self.y)
    
    def movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.movement_logic(self.x - 1, self.y)
            elif event.key == pygame.K_d:
                self.movement_logic(self.x + 1, self.y)
            elif event.key == pygame.K_w:
                self.movement_logic(self.x, self.y - 1)
            elif event.key == pygame.K_s:
                self.movement_logic(self.x, self.y + 1)
    
    def move_action(self, action):
        if action not in ACTIONS:
            return
        dx, dy = ACTIONS[action]
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(self.grid[0]) and 0 <= new_y < len(self.grid):
            if self.grid[new_y][new_x] in (0, 2, 3):
                self.x, self.y = new_x, new_y
    
    def get_player_position(self):
        return (self.x, self.y)
    
    def reset_plr(self):
        self.get_start_position()
    
    def set_position(self, pos):
        self.position = pos