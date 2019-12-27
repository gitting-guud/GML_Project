# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 12:19:15 2019

@author: Houcine's laptop
"""

from Env import  Graph
import numpy as np

class Generate_Graph :
    """ Graph types : 
    - Random_Sparse_graph : each edge has a cost 1 and random edges are romeved from the fully connected graph
    - OW : The graph  found in OW.net file in the same directory
    """
    def __init__(self, graph_type, nb_vertices = None, dropout_edge_rate = None):
        
        self.graph_type = graph_type
        
        if self.graph_type == "Random_Sparse_graph" :
            assert nb_vertices is not None
            self.V = nb_vertices
            assert dropout_edge_rate is not None 
            self.dropout_edge_rate = dropout_edge_rate
            
    def build_Random_Sparse_graph(self):

        g = Graph()
        for i in range(self.V):
            g.add(i,i)

        adj_matrix = np.zeros((V,V))
        all_edges = {}
        for i in range(1,V):
            for j in range(i,V):
                if np.random.random() > self.dropout_egde_rate :
                    adj_matrix[i,j], adj_matrix[j,i] = 1, 1
                    g.addEdge(i,j,1)
                    g.addEdge(j,i,1)
                    all_edges[(i,j)] = 1
                    all_edges[(j,i)] = 1
                    
        return g, adj_matrix, all_edges
    
    def build_OW_graph(self):
        
        f = open("OW.net")
        string = f.read()
        for row in string.split("\n"):
            names = {}
            i = 0
            if "node" in row and len(row) == 6 :
                names[row[-1]] = i
                i+=1
        
        f = open("OW.net")
        string = f.read()
        all_edges = {}
        for row in string.split("\n"):
            if "edge" in row and "-" in row:
                s, d = row[5], row[7]
                cost = int(row[15:])
                all_edges[(names[s], names[d])] = cost
                all_edges[(names[d], names[s])] = cost
        
        
        g = Graph()
        for i in range(len(names)):
            g.add(i, names[names.keys()[i]])
            
        adj_matrix = np.zeros((len(names), len(names)))
        for i in range(1,len(names)):
            for j in range(i,len(names)):
                adj_matrix[i,j], adj_matrix[j,i] = all_edges[(i,j)], all_edges[(j,i)]
                g.addEdge(i,j,all_edges[(i,j)])
                g.addEdge(j,i,all_edges[(j,i)])
        
        return g, adj_matrix, all_edges
    
    def build(self):
        
        if self.graph_type == "Random_Sparse_graph":
            return build_Random_Sparse_graph()
        
        if self.graph_type == "OW":
            return build_OW_graph()
            