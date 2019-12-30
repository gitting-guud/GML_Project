# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 02:15:44 2019

@author: Houcine's laptop
"""

import numpy as np

class Exp2_agent_part1 :
    
    def __init__(self, t, arms_adv, proba_over_arms):
        
        self.arms_adv = arms_adv #list of lists representing the playable arms
        self.t = t
        self.proba_over_arms = proba_over_arms
          
    def step(self):
        index = np.random.choice(len(self.arms_adv), p= self.proba_over_arms)
        arm_to_play = self.arms_adv[index]
        return arm_to_play
    
class Exp2_agent_part2 :
    
    def __init__(self, t, arm_played, arms_adv, cost_edges_observed, old_proba_over_arms, edge_presence_in_arm_indexes, 
                lr_type = 1):
        
        self.arms_adv = arms_adv
        self.t = t
        self.cost_edges_observed = cost_edges_observed
        self.arm_played = arm_played
        self.edge_presence_in_arm_indexes = edge_presence_in_arm_indexes
        if lr_type == 1 :
            self.lr = 1/np.sqrt(max(t,1))
        if lr_type == 2 :
            self.lr = 1/(4 * np.sqrt(max(t,1)))
        if lr_type == 3 :
            self.lr = 4 * np.sqrt(np.log(t+1)/(t+1))
        if lr_type == 4 :
            self.lr = 4 * np.sqrt(np.log(max(t,1))/max(t,1))
        if lr_type == 5 :
            self.lr = 0.1
   
        self.old_proba_over_arms = old_proba_over_arms
        
    def update_own_statistics(self):
        """Update own beliefs w.r.t the observations"""
        zhat = np.zeros(len(self.cost_edges_observed))
        for hop in range(len(self.arm_played)-1):
            s, d = self.arm_played[hop], self.arm_played[hop+1]
            index = list(self.cost_edges_observed.keys()).index((s,d))            
            denominator = 0
            indices_arms = np.where(self.edge_presence_in_arm_indexes[index]>0)[0]
            for ind in indices_arms:
                denominator += self.old_proba_over_arms[ind]
                
            zhat[index] = self.cost_edges_observed[(s,d)][hop] / denominator
        
        self.new_proba_over_arms = np.zeros(len(self.arms_adv))
        
        for j, arm in enumerate(self.arms_adv):
            self.new_proba_over_arms[j] = np.exp(-self.lr * np.dot(self.edge_presence_in_arm_indexes[:,j], zhat)) * self.old_proba_over_arms[j]
        
        self.new_proba_over_arms = self.new_proba_over_arms / self.new_proba_over_arms.sum()


        return self.new_proba_over_arms
