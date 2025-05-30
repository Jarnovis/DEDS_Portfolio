import pygame
import player
import enviroment
import agent
import matplotlib.pyplot as plt

class window:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid_width = len(grid[0])  
        self.grid_height = len(grid)
        self.blockSizeX = self.width // self.grid_width
        self.blockSizeY = self.height // self.grid_height
        self.given_grid = grid
        self.plr = player.player(self.given_grid)
        
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

                if self.given_grid[row][col] == 0:
                    pygame.draw.rect(
                        self.screen, 
                        (255, 255, 255), 
                        rect
                    )
                elif self.given_grid[row][col] == 2:
                    pygame.draw.rect(
                        self.screen, 
                        (0, 0, 0), 
                        rect
                    )
                elif self.given_grid[row][col] == 3:
                    pygame.draw.rect(
                        self.screen, 
                        (0, 255, 0), 
                        rect
                    )
                else:
                    pygame.draw.rect(
                        self.screen, 
                        (255, 0, 0), 
                        rect
                    )

                pygame.draw.rect(
                    self.screen,
                    (100, 100, 100),
                    rect,
                    1
                )
    
    def draw_plr(self):
        plr_x, plr_y = self.plr.get_player_position()
        
        rect = pygame.Rect(
            plr_x * self.blockSizeX,
            plr_y * self.blockSizeY,
            self.blockSizeX,
            self.blockSizeY
        )
    
        pygame.draw.rect(
            self.screen, 
            (100, 100, 100), 
            rect
        )

    # def run(self):
    #     running = True
        
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
                
    #             self.plr.movement(event)
            
    #         self.screen.fill((0, 0, 0))
    #         self.draw_grid()
            
            
    #         self.draw_plr()
    #         pygame.display.flip()

    #     pygame.quit()


    def run(self):
        running = True
        forced_game_over = False
        bot_num = 1
        
        env = enviroment.enviroment(self.given_grid, self.plr)
        bot = agent.agent(self.given_grid, alpha=0.1, random_factor=0.25)
        
        while running:            
            while not env.is_game_over():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                state, _ = env.get_state_and_reward()
                allowed_moves = env.allowed_states.get(state, [])
                
                print(allowed_moves)
                
                if not allowed_moves:
                    print(f"No allowed moves from {state}. Stopping.")
                    running = False
                    continue
                
                action = bot.choose_action(state, allowed_moves)
                env.update(action)
                
                state, reward = env.get_state_and_reward()
                bot.update_state_history(state, reward)
                
                self.screen.fill((0, 0, 0))
                self.draw_grid()
                self.draw_plr()
                
                font = pygame.font.SysFont(None, 24)
                text = font.render(f"Episode: {bot_num} | steps: {env.steps}", True, (255, 255, 255))
                self.screen.blit(text, (10, 10))  # (10, 10)=position

            
                pygame.display.flip()
                
                if env.steps > 350:
                    forced_game_over = True

                if env.is_game_over() or forced_game_over:
                    bot.learn()
                    env = enviroment.enviroment(self.given_grid, self.plr)
                    forced_game_over = False
                    bot_num += 1

