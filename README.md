# GML_Project
Semi-bandits for Decentralized Optimal Transport on a Graph

By KILANI AL HOUCEINE and NAOUMI SALMANE, under the supervision of Mr SEZNEC Julien

The goal is to compare, on a graph structured dataset, the behavior of 3 agents :
- A stochastic bandit agent 
- An adversarial bandit agent 
- A "hybrid" agent that uses both stategies (To be determined how it switches between the algorithms during the run)

For the first two agents, we will use the adapted versions of UCB (stochastic) "USCB" and Exp3 (adversarial) "CombExp" to the case of a semi-bandit feedback 
of R.Combes paper "Combinatorial Bandits Revisited" : https://arxiv.org/pdf/1502.03475.pdf 

For the third agent : We plan to use the algorithm presented by the paper 
"Beating Stochastic and Adversarial Semi-bandits Optimally and Simultaneously" of J.Zimmert (https://github.com/diku-dk/CombSemiBandits)

The files in this repository are then :
- Environment : The graph structed datasets on where we will run our MAB agents (We
- Agents : The codes of the different agents implemented (There a  step of adaptation of the inputs/outputs we will see if we are going to do it in the Environments level or in the Agents level)
- Comparisons : jupyter notebooks to perform the behavioural analysis of the agents and the regret analysis w.r.t to the baseline provided by the Oracle.
- Report_Presentation : The final summary reporting the figures from Comparisons and the litterature and that should be submitted and the slides of the presentation.