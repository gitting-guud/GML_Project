import numpy as np
import random

class FTRL_agent_part1 :
    
    def __init__(self, t, arms_sto, dict_hat_costs_edges, history_visited_edges, gamma=1):
        
        self.t = t # the current iteration
        self.history_visited_edges = np.array(list(history_visited_edges.values())) # The agent's own count of the edges he visited
        self.arms_sto = arms_sto # The arms/paths to reach the destination 
        self.L_hat = np.zeros(len(self.arms_sto))
        self.x = 0.5 * np.ones(len(self.arms_sto))
        self.dict_hat_costs_edges = dict_hat_costs_edges # the supposition on the costs of the edges the agent makes by himself, as a dict
        
        if not ((gamma >=0 ) and (gamma <= 1)):
            raise ValueError('Gamma should be between 0 and 1')
        else :
            self.gamma = gamma # parameter of the UCB update

    def get_learning_rate(self, t):
        return 1.0 / np.sqrt(t)

    def solve_optimization(self):

        self.x = None
        return NotImplementedError

    def sample_action(self, x):
        return NotImplementedError

    def step(self):
        self.learning_rate = self.get_learning_rate(self.t)
        self.solve_optimization()
        action = self.sample_action(self.x)
        self.t +=1
        return action

    def update_L_hat(self, action, feedback):
        
        l_hat = np.divide((np.array(feedback) + 1.0), self.x[action]) - 1
        self.L_hat += l_hat
