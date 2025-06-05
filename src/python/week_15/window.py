import pygame
import enviroment
import player
import numpy as np
import agent
import random

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
        self.steps = 0
        self.episodes = 1
        self.finishes = 0
        self.agent_game = False
        self.start_music = False
        self.music_started = False
        
        self.player_image = pygame.image.load("images/Player.jpg")
        self.player_image = pygame.transform.scale(self.player_image, (self.blockSizeX, self.blockSizeY))
        self.ob_imgs_load = [
            pygame.transform.scale(pygame.image.load("images/Alpine.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/AstonMartin.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Ferrari.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Haas.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Mclaren.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Mercedes.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/RacingBulls.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Redbull.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Sauber.jpg"), (self.blockSizeX, self.blockSizeY)),
            pygame.transform.scale(pygame.image.load("images/Williams.jpg"), (self.blockSizeX, self.blockSizeY))
        ]
        
        self.trap_images = {}
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.given_grid[row][col] == 4:
                    self.trap_images[(row, col)] = random.choice(self.ob_imgs_load)


        pygame.init()
        pygame.mixer.init()
        
        self.background_sound = pygame.mixer.music.load("sounds/background.mp3")
        
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
                    pygame.draw.rect(self.screen, color, rect)
                elif val == 1:
                    color = (100, 100, 100)
                    pygame.draw.rect(self.screen, color, rect)
                elif val == 2:
                    color = (0, 0, 0)
                    pygame.draw.rect(self.screen, color, rect)
                elif val == 3:
                    color = (0, 255, 0)
                    pygame.draw.rect(self.screen, color, rect)
                elif val == 4:
                    if self.agent_game:
                        image = self.trap_images.get((row, col))
                        if image:
                            self.screen.blit(image, rect.topleft)
                    else:
                        color = (255, 0, 0)
                        pygame.draw.rect(self.screen, color, rect)
                else:
                    color = (255, 0, 0)
                    pygame.draw.rect(self.screen, color, rect)

                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)


    def draw_plr(self):
        if self.agent_game:
            plr_x, plr_y = self.agent.current_pos
        else:
            plr_x, plr_y = self.plr.get_player_position()

        rect = pygame.Rect(
            plr_x * self.blockSizeX,
            plr_y * self.blockSizeY,
            self.blockSizeX,
            self.blockSizeY
        )
        
        if not self.agent_game:
            if self.start_music and self.music_started:
                pygame.mixer.music.stop()
                self.music_started = False
                self.start_music = False
        
            pygame.draw.rect(self.screen, (0, 0, 255), rect)  
        else:
            if not self.start_music:
                self.start_music = True
            if self.start_music and not self.music_started:
                pygame.mixer.music.play(-1)
                self.music_started = True

            self.screen.blit(self.player_image, rect.topleft)
    
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

    def run(self):
        running = True
        clock = pygame.time.Clock()
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
                    elif event.key == pygame.K_p:
                        self.agent_game = not self.agent_game
                
                if not self.agent_game:
                    self.plr.movement(event)
                
            
            if self.agent_game:
                next_position = self.agent_position()
                self.plr.set_position(next_position)

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_plr()
            
            if self.agent_game:
                self.text_agent(speed)
            else:
                self.text_plr()
                
            pygame.display.flip()

            pygame.time.delay(speed) 
        pygame.quit()
