import numpy as np
import random
import enviroment

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class agent(object):
    def __init__(self, enviroment, learning_rate=0.1, discount_factor=0.99, epsilon=0.2):
        self.env = enviroment
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_start = epsilon
        
        height = len(enviroment.GRID)
        width = len(enviroment.GRID[0])
        num_actions = len(ACTIONS)
        self.q_table = np.zeros((height, width, num_actions))
        self.actions_list = list(ACTIONS.values())
        
        self.current_pos = enviroment.START
    
    def choose_action(self, state):
        # als de int kleiner is dan epislon, random keuze
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(len(ACTIONS)))
        
        # Hoogste Q-waarde wordt gebruikt
        x, y = state
        return np.argmax(self.q_table[y, x])
    
    # Beste acties bijhouden
    def get_policy(self):
        policy = np.full((len(self.env.GRID), len(self.env.GRID[0])), ' ')
        
        for y in range(len(self.env.GRID)):
            for x in range(len(self.env.GRID[0])):
                best_action = np.argmax(self.q_table[y, x]) # Grootste Q-waarde voor de huidige positie
                if (x, y) == self.env.FINSIH:
                    policy[y, x] = 'G'  # Goal
                elif (x, y) == self.env.START:
                    policy[y, x] = 'S'  # Start
                else:
                    direction = list(ACTIONS.keys())[best_action] # Beste actie kiezen
                    policy[y, x] = direction[0]
        return policy

    # Leren met GUI
    def learn_step(self, state):
        x, y = state
        action_idx = self.choose_action(state)
        dx, dy = list(ACTIONS.values())[action_idx]

        new_x = x + dx
        new_y = y + dy

        # Checks voor muren
        if (0 <= new_x < len(self.env.GRID[0]) and
            0 <= new_y < len(self.env.GRID) and
            self.env.GRID[new_y][new_x] != 1):
            next_state = (new_x, new_y)
        else:
            next_state = (x, y)
        
        # Check voor stilstaan
        if next_state == (x, y):
            reward = -100
        else:
            reward = self.env.GRID[new_y][new_x]

        if self.env.GRID[new_y][new_x] == 3:
            reward = 100


        # Update Q-Waardes
        old_q = self.q_table[y, x, action_idx] # Huidige Q-waarde
        # Maximale Q-waarde
        # Als done, dan is er geen mogelijke uitkomst (Einde episode)
        next_max = np.max(self.q_table[next_state[1], next_state[0]])
        # reward: Standaard beloning
        # gamma * max_future_q: Hoe hoger gamma, hoe lager de extra reward, omdat er gekeken wordt naar toekomstige rewards
        # alpha: Leersnelheid
        self.q_table[y, x, action_idx] = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        
        self.current_pos = next_state
        self.epsilon = max(0.01, self.epsilon * 0.99)

        return next_state, reward
    
    def set_posistion(self, position):
        self.current_pos = position
    
    def reset(self):
        self.env.reset()
        self.__init__(self.env, self.alpha, self.gamma, self.epsilon_start)
