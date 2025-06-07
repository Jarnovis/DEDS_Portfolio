import pygame
import numpy as np
import player
import enviroment

class window_normal:
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
        self.steps = 0
        self.episodes = 1
        self.finishes = 0
        self.agent_game = False
        
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
                    color = (100, 100, 100)
                elif val == 2:
                    color = (0, 0, 0)   
                elif val == 3:
                    color = (0, 255, 0) 
                elif val == 4:
                    color = (128, 128, 0) 
                else:
                    color = (0, 255, 255)  

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1) 

    def draw_plr(self):
        if self.agent_game:
            plr_x, plr_y = self.agent.current_pos
        else:
            plr_x, plr_y = self.plr.get_player_position()
            self.agent.set_posistion((plr_x, plr_y))

        rect = pygame.Rect(
            plr_x * self.blockSizeX,
            plr_y * self.blockSizeY,
            self.blockSizeX,
            self.blockSizeY
        )

        if not self.agent_game:
            pygame.draw.rect(self.screen, (0, 0, 255), rect)
        else:
            pygame.draw.rect(self.screen, (0, 0, 200), rect)

    def text(self, text):
        font = pygame.font.SysFont(None, 24)
        lines = text.split("\n")
        
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (0, 0 + i*24))

    def text_agent(self, delay):
        text = f"Game: AGENT\nEpisode: {self.episodes} | Steps: {self.steps} | Goal reached: {self.finishes} | Deaths: {self.episodes - self.finishes - 1} | Delay: {delay}"
        self.text(text)

    def text_plr(self):
        text = "Game: PLAYER"
        self.text(text)

    def agent_position(self):
        current_pos = self.agent.current_pos
        next_pos, reward = self.agent.learn_step(current_pos)
        self.steps += 1
        
        if reward == -100 or reward == 100 or next_pos == current_pos:
            if reward == 100: 
                print("Goal reached!")
                self.agent.current_pos = self.agent.env.START
                self.steps = 0
                self.episodes += 1
                self.finishes += 1
            elif reward == -100:
                print("Hit a wall! Restarting episode.")
                self.agent.current_pos = self.agent.env.START
                self.steps = 0
                self.episodes += 1
        
        return next_pos
    
    def draw_q_values(self):
        font = pygame.font.SysFont(None, 14)
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.given_grid[y][x] == 1:  
                    continue

                q_values = self.agent.q_table[y, x]
                best_action = np.argmax(q_values)
                
                
                for i, q_val in enumerate(q_values):
                    if i == 0: 
                        pos = (x * self.blockSizeX + self.blockSizeX // 2 - 10, y * self.blockSizeY + 2)
                    elif i == 1:
                        pos = (x * self.blockSizeX + self.blockSizeX // 2 - 10, y * self.blockSizeY + self.blockSizeY - 16)
                    elif i == 2:
                        pos = (x * self.blockSizeX + 2, y * self.blockSizeY + self.blockSizeY // 2 - 8)
                    else: 
                        pos = (x * self.blockSizeX + self.blockSizeX - 30, y * self.blockSizeY + self.blockSizeY // 2 - 8)

                    if q_val == q_values[best_action]:
                        color = (0, 255, 0) 
                    elif q_val < 0:
                        color = (255, 0, 0)
                    else:
                        color = (200, 200, 200) 

                    text_str = f"{q_val:.1f}"
                    text_surface = font.render(text_str, True, color)
                    self.screen.blit(text_surface, pos)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        speed = 0
        min_steps = self.grid_width + self.grid_height * 1.5
        max_steps = max(min_steps, int(250 * (self.grid_width * self.grid_height) / 100))

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
                    elif event.key == pygame.K_p:
                        self.agent_game = not self.agent_game
                    elif event.key == pygame.K_r:
                        self.agent.reset()
                        self.steps = 0
                        self.episodes = 1
                        self.finishes = 0
                        self.given_grid = self.agent.env.GRID_NORMAL
                        self.plr = player.player(self.given_grid)
                
                if not self.agent_game:
                    self.plr.movement(event)
                
            
            if self.agent_game:
                next_position = self.agent_position()
                self.plr.set_position(next_position)

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_plr()
            
            if self.agent_game:
                self.draw_q_values()
                self.text_agent(speed)
            else:
                self.text_plr()
            
            if max_steps < self.steps:
                self.agent.set_position((1, 1))
                self.steps = 0
                self.episodes += 1
                print("Out of steps! Restarting episode.")
                
            pygame.display.flip()

            pygame.time.delay(speed) 
        pygame.quit()
