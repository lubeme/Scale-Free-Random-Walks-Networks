#!/usr/bin/python
# -*- coding: UTF-8 -*-
import networkx as nx
import random
from scipy.stats import bernoulli

__author__ = 'Luis Úbeda (http://www.github.com/lubeme)' 


def random_walks_powerlaw_cluster_graph(m,n,cc,seed=None):
    """Return random graph using Herrera-Zufiria random walks model.
    
    A Scale-free graph of n nodes is grown by attaching new nodes 
    each with m edges that are connected to existing by performing
    random walks,using only local information of the network.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    cc: int
        clustering control parameter, from 0 to 100. Increasing control
        parameter implies increasing the clustering of the graph
    seed : int, optional
        Seed for random number generator (default=None). 

    Returns
    -------
    G : Graph
        
    Notes
    -----
    The initialization is a circular graph with an odd number of nodes.
    For small values of m initial graph has at least 11 nodes.  

    References
    ----------
    .. [1] Herrera, C.; Zufiria, P.J.; , "Generating scale-free networks 
    with adjustable clustering coefficient via random walks," 
    Network Science Workshop (NSW),
    2011 IEEE , vol., no., pp.167-172, 22-24 June 2011
    """


    if m < 1 or  m >=n or cc < 0 or cc > 100:
        raise nx.NetworkXError(\
            "The network must have m>=1, m<n and "
            "cc between 0 and 100. m=%d,n=%d cc=%d"%(m,n,cc))
    if seed is not None:
        random.seed(seed)
    nCero= max(11,m)
    if nCero%2==0:
        nCero+=1
    #simulated grapfh
    G= nx.Graph()
    #list of probabilities 'pi' associated to each node 
    #representing a genetic factor
    p=bernoulli.rvs(cc/float(100),size=n)

    #Initialising the grapfh
    for i in range(nCero):
        #Ring graph
        G.add_edge(i,(i+1)%nCero)
            
    #main loop of the algorithm
    for j in range(nCero,n):
        #Choose Random node
        vs =random.randrange(0,G.number_of_nodes())
        #random walk of length>1 beginning on vs
        l = 7
        ve=vs
        for i in range(l):
            neighborsVe = G.neighbors(ve)
            ve= neighborsVe[random.randrange(0,len(neighborsVe))]
            
        markedVertices=[]
        #mark ve
        markedVertices.append(ve)
        vl=ve
        
        #Mark m nodes
        for i in range(m-1):
            #Random walk of l = [1 , 2] depending on the 
            #genetic factor of the node vl
            if p[vl] ==0:
                l=2
            else:
                l=1
            vll=vl
            #Random Walk starting on vl, avoiding already marked vertices
            while ((vll in markedVertices)):
                for k in range(l):
                    neighborsVl = G.neighbors(vll)
                    vll= neighborsVl[random.randrange(0,len(neighborsVl))]
            vl=vll
            #mark vl
            markedVertices.append(vl)
        #Add the new node    
        G.add_node(j)
        #Assign the node a pi
        #Add the m marked neighbors to vl
        for i in range(m):
            G.add_edge(j,markedVertices[i])
    return G
