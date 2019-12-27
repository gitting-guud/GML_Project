# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:24:37 2019

@author: Houcine's laptop
"""
import numpy as np
import itertools
from functools import reduce
from timeit import default_timer as timer
from tqdm import tqdm_notebook



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
           fullPath.append({
                            "path": list(path),
#                             "cost": vertex.currCost
                           })

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
    
    def __init__(self, graph, list_agents_names, adj_matrix):
        self.g = graph
        self.list_agents_names = list_agents_names
        self.adj_matrix = adj_matrix
        self.assigned = False
        
    def reset(self):
        self.nb_players = len(self.list_agents_names)
        self.agents_dicts = list()
        
    def random_assignement(self):
        
        self.reset()
        for name in self.list_agents_names :
            dico = dict()
            dico["name"] = name
            dico["infos"] = {}
            Path_not_exists = True 
            while Path_not_exists :
                start_desti = np.random.choice(list(self.g.vertices.keys()), replace = False, size = 2)
                start, destination = start_desti[0],start_desti[1]
                if len(self.g.getAllPaths(start, destination)) > 0 :
                    Path_not_exists = False
                    dico["infos"]["start"], dico["infos"]["destination"] = start, destination 
                    dico["infos"]["arms"] = self.g.getAllPaths(start, destination)
            self.agents_dicts.append(dico)
        self.assigned = True

        return self.agents_dicts

    def get_optimal_paths(self, combinatorial=True, time_limit=3):
        
        if self.assigned == False :
            raise ValueError("Agents not yet assigned to graph!")

        if combinatorial:
            list_paths = list()
            total_costs = list()
            for i in range(self.nb_players):
                list_paths.append(sorted(list(map(lambda d: d['path'], self.agents_dicts[i]["infos"]['arms'])), 
                                        key=len, reverse=False))
            paths_combinations = itertools.product(*list_paths)
            start = timer()
            j = 0
            min_cost = 99999
            aborted = False
            for list_arms_pulled_ in paths_combinations:
                j+=1
                costs = cost_calculator(list_arms_pulled=list(list_arms_pulled_), adj_matrix= self.adj_matrix).return_costs()[0]
                total_cost = sum(map(lambda x: x['cost'], list(costs.values())))
                total_costs.append(total_cost)
                if total_cost < min_cost:
                    min_cost = total_cost
                    opt_path = list(list_arms_pulled_)
                if timer() - start > time_limit:
                    print('Time depassed {} seconds, only {} combinations where tested'.format(time_limit, j))
                    aborted = True
                    break
            if not aborted :
                print('Testing {} combination of paths'.format(j))
            end = timer()
            print('Total time to compute costs:{:.2f} s'.format(end-start))
            # optimal_paths = np.argsort(total_costs)
            # print(np.sort(total_costs))
            print(' => The minimal cost is : ', min_cost)
            print(' => The optimal paths are : ', opt_path)
        else:
            pass


        return None
    
class cost_calculator :
    
    def __init__(self, list_arms_pulled, adj_matrix):
        self.adj_matrix = adj_matrix.copy()
        self.list_arms = list_arms_pulled.copy()

        # set the initial costs of edges at the round t
        self.edges_count_reset = {}
        for i in range(self.adj_matrix.shape[0]):
            for j in range(self.adj_matrix.shape[1]):
                if self.adj_matrix[i,j]>0:
#                     self.edges_count_reset[(i,j)] = 0
                    self.edges_count_reset[(i,j)] = []
        
        
    def reset(self):
        for key in self.edges_count_reset.keys():
#             s, d = key[0], key[1]
#             self.edges_count_reset[key].append(self.adj_matrix[s,d])
            self.edges_count_reset[key].append(0)
#         self.edges_count = self.edges_count_reset.copy()
        
    def padding(self, list_, nb_elements_to_pad):
        return list_ + [-99]*nb_elements_to_pad
    
    def get_max_len(self):
        max_len = -9999     
        for L in self.list_arms :
            l = len(L) 
            if l > max_len :
                max_len = l
        return max_len
    
    def cost_calculation(self):

        max_len = self.get_max_len()
        self.list_arms_padded = []
        self.costs_arms = np.zeros(len(self.list_arms))
        
        for list_ in self.list_arms :
            self.list_arms_padded.append(self.padding(list_, max_len - len(list_)))
        
        self.list_arms_padded = np.array(self.list_arms_padded)
        
        for j in range(self.list_arms_padded.shape[1]-1):
            self.reset()
            edges_time_j_jplusone = self.list_arms_padded[:,[j,j+1]]
            for i, row in enumerate(edges_time_j_jplusone) :
                row_inversed = row[::-1]
                tuple_row, tuple_row_inv = tuple(row), tuple(row_inversed)
                if tuple_row in self.edges_count_reset.keys():
                    # we have an undirected graph
                    s,d = tuple_row[0], tuple_row[1]
                    self.edges_count_reset[tuple_row][-1] += self.adj_matrix[s,d]
                    self.edges_count_reset[tuple_row_inv][-1] += self.adj_matrix[d,s]
            
            for i, row in enumerate(edges_time_j_jplusone):
                if tuple(row) in self.edges_count_reset.keys():
                    self.costs_arms[i] += self.edges_count_reset[tuple(row)][j]
      
        return self.costs_arms
                
    def return_costs(self):
        """Function that returns :
        - the total cost of the arms passed as arguments during that iteration.
        - the costs of each edge at each hop (hop = step towards the destination)
        """
        costs = self.cost_calculation()
        results = {}
        for i, arm in enumerate(self.list_arms):
            results[i] = {"path" : arm, 'cost':costs[i]}
            
        return results, self.edges_count_reset
        

