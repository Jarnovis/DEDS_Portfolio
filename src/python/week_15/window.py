import pygame

class window:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid_width = len(grid[0])  
        self.grid_height = len(grid)
        self.blockSizeX = self.width // self.grid_width
        self.blockSizeY = self.height // self.grid_height
        self.given_grid = grid
        
        pygame.init()
        
    def grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(
                    col * self.blockSizeX,
                    row * self.blockSizeY,
                    self.blockSizeX,
                    self.blockSizeY
                )

                if self.given_grid[row][col] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect) 
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)

                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

        
    def create(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My Pygame Window")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.grid()
            pygame.display.flip()

        pygame.quit()
