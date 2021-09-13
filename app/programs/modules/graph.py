import networkx as nx
import itertools
import numpy.random as rnd
import matplotlib.pyplot as plt

def complete_graph(N: int) -> nx.Graph:
  graph = nx.Graph()
   
  N_range = range(N)
   
  all_pairs = itertools.permutations(N_range, 2)
   
  graph.add_nodes_from(N_range)
  graph.add_edges_from(all_pairs)
   
  return graph

graph = complete_graph(15)

nx.draw_circular(graph, 
         node_color='y',
         node_size=750,
         with_labels=True)

plt.show()
