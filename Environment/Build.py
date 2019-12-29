# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 12:19:15 2019

@author: Houcine's laptop
"""

from .Env import  Graph
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

        adj_matrix = np.zeros((self.V,self.V))
        all_edges = {}
        for i in range(1,self.V):
            for j in range(i,self.V):
                if np.random.random() > self.dropout_edge_rate :
                    adj_matrix[i,j], adj_matrix[j,i] = 1, 1
                    g.addEdge(i,j,1)
                    g.addEdge(j,i,1)
                    all_edges[(i,j)] = 1
                    all_edges[(j,i)] = 1
                    
        return g, adj_matrix, all_edges
    
    
    def build_Sioux_Falls_graph(self):

        f = open("../Environment/SiouxFalls_flow.tntp")
        string = f.read()
        
        tab = np.array([row.split("\t") for row in string.split("\n")][1:-1])
        start_nodes = tab[:,0].astype(int)-1
        destination_nodes = tab[:,1].astype(int)-1
        nodes = np.unique(np.concatenate((start_nodes, destination_nodes)))
        
        g = Graph()
        for i in nodes :
            g.add(i,i)

        adj_matrix = np.zeros((len(nodes),len(nodes)))
        all_edges = {}
        for row in tab : 
            s = int(row[0])-1
            d = int(row[1])-1
            cost = float(row[-1])
            adj_matrix[s,d] = cost
            all_edges[(s,d)] = cost    
            g.addEdge(s,d,cost)

                    
        return g, adj_matrix, all_edges
    
    def build_OW_graph(self):
        
        f = open("../Environment/OW.net")
        string = f.read()
        names = {}
        i = 0
        for row in string.split("\n"):
            if "node" in row and len(row) == 6 :
                names[row[-1]] = i
                i+=1
        f = open("../Environment/OW.net")
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
            g.add(i, names[list(names.keys())[i]])
            
        adj_matrix = np.zeros((len(names), len(names)))
        for i in range(1,len(names)):
            for j in range(i,len(names)):
                if (i,j) in all_edges.keys():
                    adj_matrix[i,j], adj_matrix[j,i] = all_edges[(i,j)], all_edges[(j,i)]
                    g.addEdge(i,j,all_edges[(i,j)])
                    g.addEdge(j,i,all_edges[(j,i)])
        
        return g, adj_matrix, all_edges
    
    
    def build(self):
        
        if self.graph_type == "Random_Sparse_graph":
            return self.build_Random_Sparse_graph()
        
        if self.graph_type == "OW":
            return self.build_OW_graph()
        if self.graph_type == "Sioux_Falls":
            return self.build_Sioux_Falls_graph()
            