import pygame
import enviroment
import player
import numpy as np
import agent

class window:
    def __init__(self, width, height, grid, agent):
        self.width = width
        self.height = height
        self.grid_width = len(grid[0])  
        self.grid_height = len(grid)
        self.blockSizeX = self.width // self.grid_width
        self.blockSizeY = self.height // self.grid_height
        self.given_grid = grid
        self.plr = player.player(self.given_grid)
        self.agent = agent

        pygame.init()

    def create(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze")

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(
                    col * self.blockSizeX,
                    row * self.blockSizeY,
                    self.blockSizeX,
                    self.blockSizeY
                )

                val = self.given_grid[row][col]
                if val == 0:
                    color = (255, 255, 255)
                elif val == 1:
                    color = (255, 0, 0)  
                elif val == 2:
                    color = (0, 0, 0)    
                elif val == 3:
                    color = (0, 255, 0)    
                else:
                    color = (100, 100, 100) 

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    def draw_plr(self):
        plr_x, plr_y = self.agent.current_pos

        rect = pygame.Rect(
            plr_x * self.blockSizeX,
            plr_y * self.blockSizeY,
            self.blockSizeX,
            self.blockSizeY
        )
        pygame.draw.rect(self.screen, (0, 0, 255), rect)  
    
    def text(self, episodes, steps, finishes, delay):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Episode: {episodes} | Steps: {steps} | Goal reached: {finishes} | Deaths: {episodes - finishes - 1} | Delay: {delay}", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 0))


    def run(self):
        running = True
        clock = pygame.time.Clock()
        steps = 0
        episodes = 1
        finishes = 0
        speed = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if speed > 0:
                            speed -= 10
                            if speed < 0:
                                speed = 0
                    elif event.key == pygame.K_DOWN:
                        speed += 10

            current_pos = self.agent.current_pos
            next_pos, reward = self.agent.learn_step(current_pos)
            
            self.plr.set_position(next_pos)
            steps += 1

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_plr()
            self.text(episodes, steps, finishes, speed)
            pygame.display.flip()

            print(next_pos, current_pos)
            
            if reward == -100 or reward == 100 or next_pos == current_pos:
                if reward == 100: 
                    print("Goal reached!")
                    self.agent.current_pos = self.agent.env.START
                    steps = 0
                    episodes += 1
                    finishes += 1
                elif reward == -100:
                    print("Hit a wall! Restarting episode.")
                    self.agent.current_pos = self.agent.env.START
                    steps = 0
                    episodes += 1

            pygame.time.delay(speed) 
        pygame.quit()
