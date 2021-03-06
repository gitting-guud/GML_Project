import numpy as np
import matplotlib.pyplot as plt
from Environment.Env import Agent_to_graph_assignment, cost_calculator
from Environment.Build import Generate_Graph
from Agents.CombUCB_agent import *
from Agents.Exp2_agent import *
from Agents.FPL_agent import *
from Agents.Random_agent import *
from Agents.Fixed_path_agent import *
from tqdm import tqdm_notebook


def get_orig_dest(graph, size) : 
        list_des = list()
        for _ in range(size) :
            Path_not_exists = True
            while Path_not_exists :
                start, destination = np.random.choice(list(graph.vertices.keys()), replace = False, size = 2)
                
                if (len(graph.getAllPaths(start, destination)) > 0) and ((start, destination) not in list_des):
                    Path_not_exists = False
            list_des.append((start, destination))
        return list_des  

def create_graph(graph_type, number_vertices=20, dropout_edge_rate=0.9):
    assert graph_type in ['Random_Sparse_graph', 'Sioux_Falls', 'OW']
    print('Graph creation...')
    generator = Generate_Graph(graph_type=graph_type, 
                           nb_vertices= number_vertices,
                           dropout_edge_rate=dropout_edge_rate)
    g, adj_matrix, all_edges = generator.build()

    print('Graph creation : Done')
    
    print("-------------------------------------------------------------------------------------------")

    return g, adj_matrix, all_edges
def run_experiment_compar(g, adj_matrix, all_edges, assignement_type='random', assignement_dests=None, nb_iterations=100, n_sto=1, n_adv=1,                           n_hyb=1,n_rand=1, n_fix=1, exploration_parameter_stoc=1.5, lr_type_exp2 = 1, eta_hyb=0.1, Bt_hyb=0.01,                                     use_adaptif_lr_hyb=False,gamma_hyb=10.0, time_limit=60) : 
    
    print("Agents creation, {} (start, destination) assignment and all possible paths computation ...".format(assignement_type))
    
    agents_sto = ['sto{}'.format(i) for i in range(1,n_sto+1) if n_sto>0]
    agents_adv = ["adv{}".format(i) for i in range(1,n_adv+1) if n_adv>0]
    agents_hyb = ["hyb{}".format(i) for i in range(1,n_hyb+1) if n_hyb>0]
    agents_random = ["ran{}".format(i) for i in range(1,n_rand+1) if n_rand>0]
    agents_fixed = ["fix{}".format(i) for i in range(1,n_fix+1) if n_fix>0]
    
    agents = agents_sto + agents_adv + agents_hyb + agents_random + agents_fixed
    
    ind_lim = 0
    for ind_agent, agent_name in enumerate(agents):
        if ("ran" not in agent_name):
            if ("fix" not in agent_name) :
                ind_lim = ind_agent
    
    assignement = Agent_to_graph_assignment(graph=g,
                                        list_agents_names = agents, 
                                        adj_matrix=adj_matrix)

    if assignement_type=='random' :
        agents_dicts = assignement.random_assignement()
#     elif (assignement_dests is None) and (assignement_type=='fixed'): 
#         assignement_dests_ = get_orig_dest(g, size=len(agents_sto + agents_adv + agents_hyb))
#         assignement_dests_other = get_orig_dest(g, size=len(agents_random + agents_fixed))
#         agents_dicts = assignement.defined_assignement(list_destinations=assignement_dests_ + assignement_dests_other)
#     else :
#         assignement_dests_ = assignement_dests
#         assignement_dests_other = get_orig_dest(g, size=len(agents_random + agents_fixed))
#         agents_dicts = assignement.defined_assignement(list_destinations=assignement_dests_ + assignement_dests_other)

    
    print("Agents creation, {} (start, destination) assignment and all possible paths computation  : Done".format(assignement_type))
    print("-------------------------------------------------------------------------------------------")
    print("Oracle calculations ==> Global optimal paths and costs...")
    min_cost, opt_path = assignement.get_optimal_paths(combinatorial=True, time_limit=time_limit)
    opt_path_agents = cost_calculator(list_arms_pulled=opt_path, adj_matrix= adj_matrix).return_costs()[0]
    print("Oracle calculations ==> Global optimal paths and costs : Done")
    print("-------------------------------------------------------------------------------------------")
    
    summary_experiences= []
    tracker_probas_over_arms_adv = {}
    arms_possible = {}
    edge_presence_in_arm_indexes = {}

    for ind_agent, agent_name in enumerate(agents) :
        arms_possible[agent_name] = []
        for arm in agents_dicts[ind_agent]["infos"]['arms']:
            arms_possible[agent_name].append(arm["path"]) 
    
    with tqdm_notebook(range(nb_iterations), desc=f'Simulation') as trange:
        for t in trange:

            list_arms_pulled = []
            for ind_agent, agent_name in enumerate(agents) :
                if (("sto" in agent_name) or ("hyb" in agent_name)) :
                    if t==0 :
                        # initialisation
                        visits_ini = {}
                        for key in all_edges.keys():
                            visits_ini[key] = 1

                        beliefs_hat_cost_edges = {} # beliefs of each agent
                        own_history_of_visits = {} # history of visits of edges proper to each agent
                        for agent_name_ in agents :
                            beliefs_hat_cost_edges[agent_name_] = all_edges.copy()
                            own_history_of_visits[agent_name_] = visits_ini.copy() # initializing the number of visits by 1
                    if "sto" in agent_name :
                        agent_class = CombUCB_agent_part1(t=t, 
                                                          arms_sto=arms_possible[agent_name], 
                                                          dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                          history_visited_edges=own_history_of_visits[agent_name],
                                                          exploration_parameter=exploration_parameter_stoc)
                    if "hyb" in agent_name :
                        agent_class = FPL_agent_part1(t=t, 
                                                      arms=arms_possible[agent_name], 
                                                      dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                      history_visited_edges=own_history_of_visits[agent_name],
                                                      eta=eta_hyb , Bt=Bt_hyb, use_adaptif_lr=use_adaptif_lr_hyb
                                                     )
                if 'adv' in agent_name :
                    if t == 0:
                        # initialisation
                        proba_over_arms = np.ones(len(arms_possible[agent_name]))/len(arms_possible[agent_name])
                        tracker_probas_over_arms_adv[agent_name] = proba_over_arms
                    agent_class = Exp2_agent_part1(t=t,
                                                   arms_adv=arms_possible[agent_name],
                                                   proba_over_arms=tracker_probas_over_arms_adv[agent_name])
                if 'ran' in agent_name :
                    agent_class = Random_agent(arms=arms_possible[agent_name])
                if 'fix' in agent_name :
                    agent_class = Fixed_Path_agent(arms=arms_possible[agent_name], index_arm=int(agent_name[3]))

                arm_to_play = agent_class.step()
                list_arms_pulled.append(arm_to_play)


            #######################################################################################################
            # Calculating the real costs after by running the agents on the graph each one following his own path 
            # given by his update strategy

            cc = cost_calculator(list_arms_pulled=list_arms_pulled, 
                                 adj_matrix= adj_matrix)
            summary_round, history_costs_edges = cc.return_costs()
            

            k_ = list(summary_round.keys())
            v_ = list(summary_round.values())
            truncated_summary_round = {}
            for i in range(ind_lim+1):
                truncated_summary_round[k_[i]] = v_[i]
            summary_experiences.append(truncated_summary_round)
            
            total_cost = sum(map(lambda x: x['cost'], list(truncated_summary_round.values())))
            trange.set_postfix(Total_Cost=total_cost)
            #######################################################################################################    
            # Updates

            for ind_agent, agent_name in enumerate(agents) :
                if "sto" in agent_name:
                    agent_class = CombUCB_agent_part2(arm_played=list_arms_pulled[ind_agent],
                                                      cost_edges_observed=history_costs_edges,
                                                      old_dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                      old_history_visited_edges=own_history_of_visits[agent_name])

                    beliefs_hat_cost_edges[agent_name], own_history_of_visits[agent_name] = agent_class.update_own_statistics()

                if "hyb" in agent_name:
                    agent_class = FPL_agent_part2(t=t,
                                                  arm_played=list_arms_pulled[ind_agent],
                                                  cost_edges_observed=history_costs_edges,
                                                  old_dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                  old_history_visited_edges=own_history_of_visits[agent_name], 
                                                 gamma=gamma_hyb)

                    beliefs_hat_cost_edges[agent_name], own_history_of_visits[agent_name] = agent_class.update_own_statistics()

                if 'adv' in agent_name :

                    if t == 0:
                        # initialisation
                        nrows = len(history_costs_edges.keys())
                        ncols = len(arms_possible[agent_name])
                        edge_presence_in_arm_indexes[agent_name] = np.zeros((nrows, ncols))
                        for i, edge in enumerate(history_costs_edges.keys()):
                            s,d = edge[0], edge[1]
                            for j, arm in enumerate(arms_possible[agent_name]):
                                if any(arm[k]==s and arm[k+1]==d for k in range(len(arm)-1)):
                                    edge_presence_in_arm_indexes[agent_name][i,j] = 1

                    agent_class = Exp2_agent_part2(t=t,
                                                   arm_played=list_arms_pulled[ind_agent],
                                                   arms_adv=arms_possible[agent_name],
                                                   cost_edges_observed= history_costs_edges,
                                                   old_proba_over_arms=tracker_probas_over_arms_adv[agent_name],
                                                   edge_presence_in_arm_indexes=edge_presence_in_arm_indexes[agent_name],
                                                   lr_type=lr_type_exp2
                                                  )
                    tracker_probas_over_arms_adv[agent_name] = agent_class.update_own_statistics()
    
    print("Paths found by the agents :")
    s = 0
    for i in range(ind_lim+1):
        print(agents[i], " ", summary_experiences[-1][i])
        s += summary_experiences[-1][i]["cost"]
    print("Final total cost on the network :", s) 
    
    with plt.style.context('ggplot'):
        plt.figure(figsize=(12,9))

        for ind_agent, agent_name in enumerate(agents):
            if ind_agent <=ind_lim :
                plt.plot(range(nb_iterations-1),
                         [summary_experiences[t][ind_agent]["cost"] for t in range(nb_iterations-1)],
                         label = agent_name + ' Optimal_cost_found = {:.1f}'.format(opt_path_agents[ind_agent]['cost']))
        plt.legend()
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.ylim(ymin=0) 
        plt.title('Evolution of agents cost')
        plt.show()
        
    with plt.style.context('ggplot'):
        plt.figure(figsize=(12,9))
        total_costs = list()
        for t in range(nb_iterations-1):
            cost = sum([summary_experiences[t][ind_agent]["cost"] for ind_agent in range(ind_lim+1)])
            total_costs.append(cost)

        plt.plot(total_costs)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.ylim(ymin=0) 
        plt.title('Evolution of total cost | Oracle\'s Optimal cost : {:.1f} | optimal_cost_found= {:.1f}'.format(min_cost,s))
        plt.show()

    print("****************************************************************************************************************************")
    return summary_experiences


def run_experiment(graph_type, number_vertices=20, dropout_edge_rate=0.9, nb_iterations=100, n_sto=1, n_adv=1, n_hyb=1, 
                   n_rand=1, n_fix=1, exploration_parameter_stoc=1.5, lr_type_exp2 = 1, eta_hyb=0.1, Bt_hyb=0.01, use_adaptif_lr_hyb=False,
                  gamma_hyb=10.0, time_limit=60) : 
    
    assert graph_type in ['Random_Sparse_graph', 'Sioux_Falls', 'OW']
    print('Graph creation...')
    generator = Generate_Graph(graph_type=graph_type, 
                           nb_vertices= number_vertices,
                           dropout_edge_rate=dropout_edge_rate)
    g, adj_matrix, all_edges = generator.build()
    print('Graph creation : Done')
    
    print("-------------------------------------------------------------------------------------------")
    print("Agents creation, random (start, destination) assignment and all possible paths computation ...")
    
    agents_sto = ['sto{}'.format(i) for i in range(1,n_sto+1) if n_sto>0]
    agents_adv = ["adv{}".format(i) for i in range(1,n_adv+1) if n_adv>0]
    agents_hyb = ["hyb{}".format(i) for i in range(1,n_hyb+1) if n_hyb>0]
    agents_random = ["ran{}".format(i) for i in range(1,n_rand+1) if n_rand>0]
    agents_fixed = ["fix{}".format(i) for i in range(1,n_fix+1) if n_fix>0]
    
    agents = agents_sto + agents_adv + agents_hyb + agents_random + agents_fixed
    
    ind_lim = 0
    for ind_agent, agent_name in enumerate(agents):
        if ("ran" not in agent_name):
            if ("fix" not in agent_name) :
                ind_lim = ind_agent
    
    assignement = Agent_to_graph_assignment(graph=g,
                                        list_agents_names = agents, 
                                        adj_matrix=adj_matrix)
    agents_dicts = assignement.random_assignement()
    print("Agents creation, random (start, destination) assignment and all possible paths computation  : Done")
    print("-------------------------------------------------------------------------------------------")
    
    print("Oracle calculations ==> Global optimal paths and costs...")
    min_cost, opt_path = assignement.get_optimal_paths(combinatorial=True, time_limit=time_limit)
    opt_path_agents = cost_calculator(list_arms_pulled=opt_path, adj_matrix= adj_matrix).return_costs()[0]
    print("Oracle calculations ==> Global optimal paths and costs : Done")
    print("-------------------------------------------------------------------------------------------")
    
    summary_experiences= []
    tracker_probas_over_arms_adv = {}
    arms_possible = {}
    edge_presence_in_arm_indexes = {}

    for ind_agent, agent_name in enumerate(agents) :
        arms_possible[agent_name] = []
        for arm in agents_dicts[ind_agent]["infos"]['arms']:
            arms_possible[agent_name].append(arm["path"]) 
    
    with tqdm_notebook(range(nb_iterations), desc=f'Simulation') as trange:
        for t in trange:

            list_arms_pulled = []
            for ind_agent, agent_name in enumerate(agents) :
                if (("sto" in agent_name) or ("hyb" in agent_name)) :
                    if t==0 :
                        # initialisation
                        visits_ini = {}
                        for key in all_edges.keys():
                            visits_ini[key] = 1

                        beliefs_hat_cost_edges = {} # beliefs of each agent
                        own_history_of_visits = {} # history of visits of edges proper to each agent
                        for agent_name_ in agents :
                            beliefs_hat_cost_edges[agent_name_] = all_edges.copy()
                            own_history_of_visits[agent_name_] = visits_ini.copy() # initializing the number of visits by 1
                    if "sto" in agent_name :
                        agent_class = CombUCB_agent_part1(t=t, 
                                                          arms_sto=arms_possible[agent_name], 
                                                          dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                          history_visited_edges=own_history_of_visits[agent_name],
                                                          exploration_parameter=exploration_parameter_stoc)
                    if "hyb" in agent_name :
                        agent_class = FPL_agent_part1(t=t, 
                                                      arms=arms_possible[agent_name], 
                                                      dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                      history_visited_edges=own_history_of_visits[agent_name],
                                                      eta=eta_hyb , Bt=Bt_hyb, use_adaptif_lr=use_adaptif_lr_hyb
                                                     )
                if 'adv' in agent_name :
                    if t == 0:
                        # initialisation
                        proba_over_arms = np.ones(len(arms_possible[agent_name]))/len(arms_possible[agent_name])
                        tracker_probas_over_arms_adv[agent_name] = proba_over_arms
                    agent_class = Exp2_agent_part1(t=t,
                                                   arms_adv=arms_possible[agent_name],
                                                   proba_over_arms=tracker_probas_over_arms_adv[agent_name])
                if 'ran' in agent_name :
                    agent_class = Random_agent(arms=arms_possible[agent_name])
                if 'fix' in agent_name :
                    agent_class = Fixed_Path_agent(arms=arms_possible[agent_name], index_arm=int(agent_name[3]))

                arm_to_play = agent_class.step()
                list_arms_pulled.append(arm_to_play)


            #######################################################################################################
            # Calculating the real costs after by running the agents on the graph each one following his own path 
            # given by his update strategy

            cc = cost_calculator(list_arms_pulled=list_arms_pulled, 
                                 adj_matrix= adj_matrix)
            summary_round, history_costs_edges = cc.return_costs()
            

            k_ = list(summary_round.keys())
            v_ = list(summary_round.values())
            truncated_summary_round = {}
            for i in range(ind_lim+1):
                truncated_summary_round[k_[i]] = v_[i]
            summary_experiences.append(truncated_summary_round)
            
            total_cost = sum(map(lambda x: x['cost'], list(summary_round.values())))
            trange.set_postfix(Total_Cost=total_cost)
            #######################################################################################################    
            # Updates

            for ind_agent, agent_name in enumerate(agents) :
                if "sto" in agent_name:
                    agent_class = CombUCB_agent_part2(arm_played=list_arms_pulled[ind_agent],
                                                      cost_edges_observed=history_costs_edges,
                                                      old_dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                      old_history_visited_edges=own_history_of_visits[agent_name])

                    beliefs_hat_cost_edges[agent_name], own_history_of_visits[agent_name] = agent_class.update_own_statistics()

                if "hyb" in agent_name:
                    agent_class = FPL_agent_part2(t=t,
                                                  arm_played=list_arms_pulled[ind_agent],
                                                  cost_edges_observed=history_costs_edges,
                                                  old_dict_hat_costs_edges=beliefs_hat_cost_edges[agent_name],
                                                  old_history_visited_edges=own_history_of_visits[agent_name], 
                                                 gamma=gamma_hyb)

                    beliefs_hat_cost_edges[agent_name], own_history_of_visits[agent_name] = agent_class.update_own_statistics()

                if 'adv' in agent_name :

                    if t == 0:
                        # initialisation
                        nrows = len(history_costs_edges.keys())
                        ncols = len(arms_possible[agent_name])
                        edge_presence_in_arm_indexes[agent_name] = np.zeros((nrows, ncols))
                        for i, edge in enumerate(history_costs_edges.keys()):
                            s,d = edge[0], edge[1]
                            for j, arm in enumerate(arms_possible[agent_name]):
                                if any(arm[k]==s and arm[k+1]==d for k in range(len(arm)-1)):
                                    edge_presence_in_arm_indexes[agent_name][i,j] = 1

                    agent_class = Exp2_agent_part2(t=t,
                                                   arm_played=list_arms_pulled[ind_agent],
                                                   arms_adv=arms_possible[agent_name],
                                                   cost_edges_observed= history_costs_edges,
                                                   old_proba_over_arms=tracker_probas_over_arms_adv[agent_name],
                                                   edge_presence_in_arm_indexes=edge_presence_in_arm_indexes[agent_name],
                                                   lr_type=lr_type_exp2
                                                  )
                    tracker_probas_over_arms_adv[agent_name] = agent_class.update_own_statistics()
    
    print("Paths found by the agents :")
    s = 0
    for i in range(ind_lim+1):
        print(agents[i], " ", summary_experiences[-1][i])
        s += summary_experiences[-1][i]["cost"]
    print("Final total cost on the network :", s) 
    
    with plt.style.context('ggplot'):
        plt.figure(figsize=(12,9))

        for ind_agent, agent_name in enumerate(agents):
            if ind_agent <=ind_lim :
                plt.plot(range(nb_iterations-1),
                         [summary_experiences[t][ind_agent]["cost"] for t in range(nb_iterations-1)],
                         label = agent_name + ' Optimal_cost_found = {:.1f}'.format(opt_path_agents[ind_agent]['cost']))
        plt.legend()
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.ylim(ymin=0) 
        plt.title('Evolution of agents cost')
        plt.show()
        
    with plt.style.context('ggplot'):
        plt.figure(figsize=(12,9))
        total_costs = list()
        for t in range(nb_iterations-1):
            cost = sum([summary_experiences[t][ind_agent]["cost"] for ind_agent in range(ind_lim+1)])
            total_costs.append(cost)

        plt.plot(total_costs)
        plt.xlabel('Iterations')
        plt.ylabel('Cost')
        plt.ylim(ymin=0) 
        plt.title('Evolution of total cost | Oracle\'s Optimal cost : {:.1f} | optimal_cost_found= {:.1f}'.format(min_cost,s))
        plt.show()

    print("****************************************************************************************************************************")
    return summary_experiences