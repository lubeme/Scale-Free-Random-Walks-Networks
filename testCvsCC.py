import sys
import networkx as nx
import matplotlib.pyplot as plt
import SFRWNetwork as sfn

iters = 10

#clustering vs cc test

maxClustCC=100
clustcc=[0]*(maxClustCC+1)

for k in xrange ( 0, iters):
	for i in xrange (0, (maxClustCC+1)):
		G= sfn.random_walks_powerlaw_cluster_graph(2,1000,i)
		clustcc[i]+=nx.average_clustering(G)/iters
		
	print "iter",k


x = range(0,len(clustcc))
y = clustcc
plt.plot(x,y,"ko",label = "m = 2")
plt.savefig("archivo",format="png")
plt.show()
