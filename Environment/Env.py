# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:24:37 2019

@author: Houcine's laptop
"""
import numpy as np

class Vertex:
    """The vertex used in the graph class"""
    def __init__(self, key, data):
       self.adjancencyList = {}
       self.key = key
       self.data = data
       self.currCost = 0  # stores own weight added with followers in path

    def connect(self, otherVertex, weight):
       self.adjancencyList[otherVertex] = weight

    def get_connections(self):
       return self.adjancencyList.keys()

    def get_cost(self, vertex):
       return self.adjancencyList[vertex]

class Graph:     
    """
    This class is a weighted directed graph that is
    supposed to be able to find all paths between two nodes

    * The graph sorts all the paths by weight
    * The graphs vertices uses keys to allow duplicates of data
    * The graphs depth first search is based on recursion"""

    """graph used to find all paths between two nodes using DFS"""
    def __init__(self):
       self.numberOfVertices = 0
       self.vertices = {}

    def add(self, key, data):
       """adds a vertex to graph and saves vertex based on unique key"""
       if key not in self.vertices:
           self.numberOfVertices += 1
           self.vertices[key] = Vertex(key, data)
           return True

       return False

    def addEdge(self, fromVertex, toVertex, weight):
       """connects two vertices"""
       if fromVertex in self.vertices and toVertex in self.vertices:
           self.vertices[fromVertex].connect(toVertex, weight)
           return True

       return False

    def getAllPaths(self, start, end):
       return self.dfs(start, end, [], [], [])

    def getAllPathsSorted(self, start, end):
       res = self.dfs(start, end, [], [], [])
       return sorted(res, key=lambda k: k['cost'])

    def dfs(self, currVertex, destVertex, visited, path, fullPath):
       """finds all paths between two nodes, returns all paths with their respective cost"""

       # get vertex, it is now visited and should be added to path
       vertex = self.vertices[currVertex]
       visited.append(currVertex)
       path.append(vertex.data)

       # save current path if we found end
       if currVertex == destVertex:
           fullPath.append({"path": list(path), "cost": vertex.currCost})

       for i in vertex.get_connections():
           if i not in visited:
               self.vertices[i].currCost = vertex.get_cost(i) + vertex.currCost
               self.dfs(i, destVertex, visited, path, fullPath)

       # continue finding paths by popping path and visited to get accurate paths
       path.pop()
       visited.pop()

       if not path:
           return fullPath
       
        
class Agent_to_graph_assignment :
    
    def __init__(self, graph, list_agents_names):
        self.g = graph
        self.list_agents_names = list_agents_names
        
    def reset(self):
        self.agents_dicts = list()
        
    def random_assignement(self):
        
        self.reset()
        for name in self.list_agents_names :
            dico = dict()
            dico["name"] = name
            Path_not_exists = True 
            while Path_not_exists :
                start_desti = np.random.choice(list(self.g.vertices.keys()), replace = False, size = 2)
                start, destination = start_desti[0],start_desti[1]
                if len(self.g.getAllPaths(start, destination)) > 0 :
                    Path_not_exists = False
                    dico["start"], dico["destination"] = start, destination 
                    dico["arms"] = self.g.getAllPaths(start, destination)
            self.agents_dicts.append(dico)
        
        return self.agents_dicts
    
    

