import maze

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class enviroment:
    def __init__(self, grid, values):
        self.GRID = self.place_rewards(grid)
        self.START = self.find_position(grid, 2)
        self.FINSIH = self.find_position(grid, 3)
        self.VALUES = values
        self.GRID_NORMAL = grid
    
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
    # Obstakels: -10
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
                elif grid[y][x] == 4:
                    rewards[y][x] = -10
        
        return rewards
    
    def reset(self):
        print(self.GRID)
        self.__init__(maze.maze().generate_random_maze(self.VALUES), self.VALUES)
        print(self.GRID)