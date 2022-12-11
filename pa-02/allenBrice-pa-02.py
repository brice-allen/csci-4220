# ##  Libraries

# import networkx as nx
# from networkx.algorithms.community.centrality import girvan_newman
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import time 
# import pprint

# ##  load graph and establish format
# karate_graph = nx.karate_club_graph()
# karate_layout = nx.spring_layout(karate_graph)

# ## display info
# print(nx.info(karate_graph))

# ## using the built in karate club graph
# karate_graph = nx.karate_club_graph()

# ##  Girvan Newman Algo
# communities = girvan_newman(karate_graph)

# ## List of nodes
# node_groups = []

# for comm in next(communities):
#     node_groups.append(list(comm))

# this_dict = dict()
# this_dict["Community 0: "] = node_groups[0]
# this_dict["Community 1: "] = node_groups[1]

# ## sloppy way to zip a title to each sub-list
# for dic in this_dict:
#     print(dic, this_dict[dic])

# ## List of colors
# color_map = []
# for node in karate_graph:
#     if node in node_groups[0]:
#         color_map.append('mediumvioletred')
#     else:
#         color_map.append('cornflowerblue')

# ## Draw, display, and save graph
# nx.draw(karate_graph,node_color=color_map, with_labels = True)
# plt.show()
# plt.savefig("gNewman.png")

## without built in karate club graph


import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

import matplotlib.pyplot as plt

karate_graph = nx.read_gml('karate.gml', label = 'id')

##  Girvan Newman Algo
communities = girvan_newman(karate_graph)

## List of nodes
node_groups = []

for comm in next(communities):
    node_groups.append(list(comm))

this_dict = dict()
this_dict["Community 0: "] = node_groups[0]
this_dict["Community 1: "] = node_groups[1]

## display info 
## print(nx.info(karate_graph)) deprecated function
print('Graph with ', len(karate_graph.nodes()), 'nodes and ',  len(karate_graph.edges()),'edges.')

## lazy way to zip a title to each sub-list
for dic in this_dict:
    print(dic, this_dict[dic])

## List of colors
color_map = []
for node in karate_graph:
    if node in node_groups[0]:
        color_map.append('mediumvioletred')
    else:
        color_map.append('cornflowerblue')

nx.draw_networkx(karate_graph, node_color=color_map, with_labels = True)
plt.show()
plt.savefig("gNewmanOut.png")


