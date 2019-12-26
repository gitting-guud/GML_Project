import numpy as np
import random

class FTRL_agent_part1 :
    
    def __init__(self, t, arms_sto, dict_hat_costs_edges, history_visited_edges, gamma=1):
        
        self.t = t # the current iteration
        self.history_visited_edges = np.array(list(history_visited_edges.values())) # The agent's own count of the edges he visited
        self.arms_sto = arms_sto # The arms/paths to reach the destination 
        self.L_hat = np.zeros(len(self.arms_sto))
        self.dict_hat_costs_edges = dict_hat_costs_edges # the supposition on the costs of the edges the agent makes by himself, as a dict
        
        if not ((gamma >=0 ) and (gamma <= 1)):
            raise ValueError('Gamma should be between 0 and 1')
        else :
            self.gamma = gamma # parameter of the UCB update

    def upper_confidence_bound(self):
        return NotImplementedError
  
    def update_L_hat(self, feedback):
        
        l_hat = None
        self.L_hat += l_hat

    def step(self):
        return NotImplementedError
    
    def get_learning_rate(self, t):
        return 1.0 / np.sqrt(t)

    def solve_optimization(self):
        return NotImplementedError