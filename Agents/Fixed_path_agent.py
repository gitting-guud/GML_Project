import numpy as np

class Fixed_Path_agent :
    
    def __init__(self, arms, index_arm):
        
        self.arms = arms # The arms/paths to reach the destination
        self.index_arm = index_arm

    def step(self):
        # Choose a random action
        if self.index_arm <= len(self.arms):
            action = self.arms[self.index_arm-1]
        else :
            action = self.arms[0]
        

        return action


