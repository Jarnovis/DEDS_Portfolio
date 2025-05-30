import numpy as np

ACTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2):
        self.state_history = [((0, 0), 0)]
        self.alpha = alpha
        self.random_factor = random_factor
        
        self.G = {}
        self.init_reward(states)
    
    def init_reward(self, states):
        for i, row in enumerate(states):
            for j, col in enumerate(row):
                self.G[(j, i)] = np.random.uniform(high=1.0, low=0.1)
    
    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))
    
    def learn(self):
        target = 0
        a = self.alpha
        
        for state, reward in reversed(self.state_history):
            self.G[state] = self.G[state] + a * (target - self.G[state])
        
        self.state_history = []
        self.random_factor -= 10e-5
    
    def choose_action(self, state, allowed_moves):
        next_move = None
        n = np.random.random()
        
        if n < self.random_factor:
            next_move = np.random.choice(allowed_moves)
        else:
            maxG = -10e15
            
            for action in allowed_moves:
                new_state = tuple([sum(x) for x in zip(state, ACTIONS[action])])
                
                if self.G[new_state] >= maxG:
                    next_move = action
                    maxG = self.G[new_state] 
        
        return next_move
        