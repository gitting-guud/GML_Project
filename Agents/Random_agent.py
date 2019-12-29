import numpy as np

class Random_agent :
    
    def __init__(self, arms):
        
        self.arms = arms # The arms/paths to reach the destination


    def step(self):
        # Choose a random action
        action = np.random.choice(self.arms)

        return action


