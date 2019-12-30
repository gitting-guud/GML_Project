import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
truncexp = stats.truncexpon

class FPL_agent_part1 :
    
    def __init__(self, t, arms, dict_hat_costs_edges, history_visited_edges, eta=0.1 , Bt=0.01,
                use_adaptif_lr=False):
        
        self.t = t # the current iteration
        self.history_visited_edges = np.array(list(history_visited_edges.values())) # The agent's own count of the edges he visited
        self.dict_hat_costs_edges = dict_hat_costs_edges # the supposition on the costs of the edges the agent makes by himself, as a dict
        self.arms = arms # The arms/paths to reach the destination
        self.hat_cost_arms = np.zeros(len(self.arms)) 
        self.L = len(self.dict_hat_costs_edges)
        self.eta = eta # Parameter acting on perturbation vectors
        # self.gamma = gamma # Parameter for exploration  
        self.Bt = Bt
        self.use_adaptif_lr = use_adaptif_lr

    def get_learning_rate(self):
        return 1.0 / np.sqrt(self.t + 1)


    def update_costs_arms(self, U):
        """Updates the costs of each possible arm of this agent """
        for j,arm in enumerate(self.arms):
            length_arm = len(arm)
            cost = 0
            for i in range(length_arm -1):
                s, d = arm[i], arm[i+1]
                index_edge = list(self.dict_hat_costs_edges.keys()).index((s,d))
                cost+=U[index_edge]
            self.hat_cost_arms[j] = cost
    
    def choose_arm(self):
        """Return the arm that costs the least """
        return self.arms[np.argmin(self.hat_cost_arms)]


    def step(self):
        # Draw perturbation vector 
        Z = truncexp.rvs(self.Bt, self.L) 
        L_hat = np.array(list(self.dict_hat_costs_edges.values()))
        if self.use_adaptif_lr:
            edges_optim = self.get_learning_rate() * L_hat - Z
        else:
            edges_optim = self.eta * L_hat - Z
        self.update_costs_arms(edges_optim)
        action = self.choose_arm()

        return action


class FPL_agent_part2 :
    
    def __init__(self, t, arm_played, cost_edges_observed, old_dict_hat_costs_edges, old_history_visited_edges, gamma=10.0):
        
        self.t = t
        self.arm_played = arm_played
        self.cost_edges_observed = cost_edges_observed
        self.old_dict_hat_costs_edges = old_dict_hat_costs_edges
        self.old_history_visited_edges = old_history_visited_edges
        self.gamma = gamma
        
    def update_own_statistics(self):
        """Update own beliefs w.r.t the observations"""
        for hop in range(len(self.arm_played)-1):
            s, d = self.arm_played[hop], self.arm_played[hop+1]
            self.old_history_visited_edges[(s,d)]+=1
            self.old_dict_hat_costs_edges[(s,d)] += self.old_dict_hat_costs_edges[(s,d)] \
                                                    / ((self.old_history_visited_edges[(s,d)] / (self.t+1)) + self.gamma) 
        
        return self.old_dict_hat_costs_edges, self.old_history_visited_edges



