import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def result(func):
    def wrapper(matrix, **params):
        fig = plt.figure(figsize=(9,6))
        ax = fig.add_subplot()
        matrix = np.matrix(matrix)
        G = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph)
        labels = {x: x+1 for x in range(G.number_of_nodes())}

        result = func(G, ax, labels=labels, **params)

        return fig, result
    return wrapper

    
@result
def create(G, ax, labels):
    nx.draw_circular(G, ax=ax, labels=labels)
    return "Граф построен."

@result
def planar(G, ax, labels):
    try:
        nx.draw_planar(G, ax=ax, labels=labels)
        return "Граф планарный."
    except nx.NetworkXException as e:
        nx.draw_circular(G, ax=ax, labels=labels)
        return "Граф не планарный."

@result
def chromatic(G, ax, labels):
    colors = ['red', 'blue', 'green', 'yellow',  'black', 'pink', 'orange', 'white',
        'gray', 'purple', 'brown', 'navy']
    colors_of_nodes = {}
    
    def coloring(node, color):
        nonlocal G, colors_of_nodes
        for neighbor in G.neighbors(node):
            color_of_neighbor = colors_of_nodes.get(neighbor, None)
            if color_of_neighbor == color:
                return False
        return True

    for node in G.nodes():
        for color in colors:
           if coloring(node, color):
              colors_of_nodes[node] = color

    nx.draw_circular(G, ax=ax, labels=labels, cmap=plt.get_cmap('viridis'),
            node_color=colors_of_nodes.values())
    return f"Хроматическое число равно {len(set(colors_of_nodes.values()))}."