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
        
        height = len(enviroment.GRID)
        width = len(enviroment.GRID[0])
        num_actions = len(ACTIONS)
        self.q_table = np.zeros((height, width, num_actions))
        self.actions_list = list(ACTIONS.values())
        
        self.current_pos = enviroment.START
        
        print(f"GRID: {self.env.GRID}")
    
    def choose_action(self, state):
        # als de int kleiner is dan epislon, random keuze
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(len(ACTIONS)))
        
        # Hoogste Q-waarde wordt gebruikt
        x, y = state
        return np.argmax(self.q_table[y, x])
    
    def learn(self, episodes=1000):
        successes = 0 
        
        for episode in range(episodes):
            state = self.env.START
            self.current_pos = self.env.START
            done = False
            steps = 0
            
            # Steeds minder ontdekken naarmate de episodes stijgen
            self.epsilon = max(0.01, self.epsilon * 0.995)
            
            while not done and steps < 1000:
                action_idx = self.choose_action(state)
                dx, dy = self.actions_list[action_idx]
                new_x = state[0] + dx
                new_y = state[1] + dy

                new_state = state

                # Checken of gekozen actie veilig is
                # Binnen het speelveld
                if 0 <= new_x < len(self.env.GRID[0]) and 0 <= new_y < len(self.env.GRID):
                    cell_value = self.env.GRID[new_y][new_x]

                    # Veilige actie
                    if cell_value != -100:
                        new_state = (new_x, new_y)

                        # Finish bereikt
                        if cell_value == 100:
                            reward = 100
                            done = True
                            successes += 1
                        # Nieuw vakje bereikt (pad)
                        else:
                            reward = -1
                    # In een muur gelopen
                    else:
                        reward = -100 
                        done = True
                # Buiten het speelveld
                else:
                    reward = -100 
                    done = True

                # Huidige Q-waarde
                old_q = self.q_table[state[1], state[0], action_idx]
                # Maximale Q-waarde
                # Als done, dan is er geen mogelijke uitkomst (Einde episode)
                max_future_q = np.max(self.q_table[new_state[1], new_state[0]]) if not done else 0
                # reward: Standaard beloning
                # gamma * max_future_q: Hoe hoger gamma, hoe lager de extra reward, omdat er gekeken wordt naar toekomstige rewards
                # alpha: Leersnelheid
                new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
                self.q_table[state[1], state[0], action_idx] = new_q

                state = new_state
                steps += 1


        
        print(f"Runs: {episodes} | Succes: {successes} | Succes %: {successes / episodes * 100}%")
    
    def get_policy(self):
        # Create a policy map of best actions
        policy = np.full((len(self.env.GRID), len(self.env.GRID[0])), ' ')
        for y in range(len(self.env.GRID)):
            for x in range(len(self.env.GRID[0])):
                best_action = np.argmax(self.q_table[y, x])
                if (x, y) == self.env.FINSIH:
                    policy[y, x] = 'G'  # Goal
                elif (x, y) == self.env.START:
                    policy[y, x] = 'S'  # Start
                else:
                    direction = list(ACTIONS.keys())[best_action]
                    policy[y, x] = direction[0]
        return policy

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


        # Update Q-Waardes (Zie Q-waardes in learn voor uitleg)  
        old_q = self.q_table[y, x, action_idx]
        next_max = np.max(self.q_table[next_state[1], next_state[0]])
        self.q_table[y, x, action_idx] = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        
        self.current_pos = next_state
        self.epsilon = max(0.01, self.epsilon * 0.99)

        return next_state, reward


# Create environment
env = enviroment.enviroment([
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
])

# Create Q-learning agent
bot = agent(env)

# Train the agent
bot.learn(episodes=1000)

# Show the learned policy
policy = bot.get_policy()
for row in policy:
    print(' '.join(row))

