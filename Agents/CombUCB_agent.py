# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 16:01:57 2019

@author: Houcine's laptop
"""

import numpy as np

class CombUCB_agent_part1 :
    
    def __init__(self, t, arms_sto, dict_hat_costs_edges, history_visited_edges, exploration_parameter):
        
        self.t = t # the current iteration
        self.history_visited_edges = np.array(list(history_visited_edges.values())) # The agent's own count of the edges he visited
        self.arms_sto = arms_sto # The arms/paths to reach the destination 
        self.hat_cost_arms = np.zeros(len(self.arms_sto))
        self.dict_hat_costs_edges = dict_hat_costs_edges # the supposition on the costs of the edges the agent makes by himself, as a dict
        
        self.exploration_parameter = exploration_parameter # parameter of the UCB update
        
    def upper_confidence_bound(self):
        
        bound = np.sqrt(self.exploration_parameter * np.log(self.t) / self.history_visited_edges)
        U = np.array(list(self.dict_hat_costs_edges.values())) + bound
        return U
  
    def update_costs_arms(self, U):
        """Updates the costs of each possible arm of this agent by his own beliefs using UCBounds"""
        for j,arm in enumerate(self.arms_sto):
            length_arm = len(arm)
            cost = 0
            for i in range(length_arm -1):
                s, d = arm[i], arm[i+1]
                index_edge = list(self.dict_hat_costs_edges.keys()).index((s,d))
                cost+=U[index_edge]
            self.hat_cost_arms[j] = cost
            
    def choose_shortest_path(self):
        """Return the arm that costs the least """
        return self.arms_sto[np.argmin(self.hat_cost_arms)]

    def step(self):
        U = self.upper_confidence_bound()
        self.update_costs_arms(U)
        arm_to_play = self.choose_shortest_path()
        return arm_to_play
    
class CombUCB_agent_part2 :
    
    def __init__(self, arm_played, cost_edges_observed, old_dict_hat_costs_edges, old_history_visited_edges):
        
        self.arm_played = arm_played
        self.cost_edges_observed = cost_edges_observed
        self.old_dict_hat_costs_edges = old_dict_hat_costs_edges
        self.old_history_visited_edges = old_history_visited_edges
        
    def update_own_statistics(self):
        """Update own beliefs w.r.t the observations"""
        for hop in range(len(self.arm_played)-1):
            s, d = self.arm_played[hop], self.arm_played[hop+1]
            self.old_history_visited_edges[(s,d)]+=1
            self.old_dict_hat_costs_edges[(s,d)] = ((self.old_history_visited_edges[(s,d)]-1)*self.old_dict_hat_costs_edges[(s,d)] + self.cost_edges_observed[(s,d)][hop])/self.old_history_visited_edges[(s,d)]
        
        return self.old_dict_hat_costs_edges, self.old_history_visited_edges
