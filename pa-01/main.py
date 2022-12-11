import networkx as nx  ##  version 2.4 library for studying graphs and networks

infile = open('dataset/cambridge_net.txt', "r+b")

cam_net = nx.read_adjlist(infile, create_using=nx.DiGraph(), nodetype=int)

thisdict = dict(cam_net.adj)

infile.close()

N = cam_net.order()

K = cam_net.number_of_edges()

avg_deg = float(K)/N

print("Nodes:", N)

print("Edges:", K)

print("Average degree:", round(avg_deg, 5))  ## rounded for aesthetic 

print("SCC:", nx.number_strongly_connected_components(cam_net))

print("WCC:", nx.number_weakly_connected_components(cam_net))


