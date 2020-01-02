# GML_Project
Semi-bandits for Decentralized Optimal Transport on a Graph

By KILANI AL HOUCEINE and NAOUMI SALMANE, under the supervision of Mr SEZNEC Julien

In this project, we consider a mass (e.g. people) transporting on a resistive graph.From a global perspective, a central planner might be interested in choosing eachroute to minimize the global cost (quadratic in each edge flow).  The constraintthat each unit of mass starts from its starting node and successfully reaches itsendpoint can be formulated as a linear constraint. Hence, this is a standard convexoptimization problem.  Nonetheless, in a decentralized setting, each player willchoose its route to minimize its local cost (linear in the flow of each visited edge).To do so, players are not allowed to communicate and are hence doomed to tryroutes sequentially. Moreover, at each try, all the players choose a route and onlyobserve the flow in the visited edges (semi-bandit feedback). The cost of a route istherefore dependent on the other players actions. Hence, rewards are not stochastic,but probably not fully adversarial as well.

For the [agents](https://github.com/gitting-guud/GML_Project/tree/master/Agents) :
- Stochastic agent : [UCB1](http://karthikabinavs.xyz/surveySemiBandit.pdf)
- Adversarial agent : [Exp2](https://arxiv.org/pdf/1204.4710.pdf)
- Hybdrid agent : [FPL-Trix](https://github.com/alohia/combandits/blob/master/report/report.pdf)

For the [environments](https://github.com/gitting-guud/GML_Project/tree/master/Environment), we implemented the following graphs :
- Random Sparse Graph : a fully connected graph where we discard randomly a fraction of the edges. 
- OW Network 
- Sioux Falls network 

We perform [comparisons](https://github.com/gitting-guud/GML_Project/tree/master/Comparisons) by launching the agents on the environments and get figures and [images](https://github.com/gitting-guud/GML_Project/tree/master/Images)

