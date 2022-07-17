import json

import networkx as nx
import numpy as np
import plotly
import plotly.graph_objects as go
import sympy as sp
from app.programs.utils import params_algorithms, register_algorithms


def result(func):
    def wrapper(params):
        fig = go.Figure()
        matrix = np.matrix(
            [[int(x) for x in row.split()] for row in params["matrix"].split("\r\n")]
        )
        G = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph)

        # result = func(G, None, labels=labels)
        Num_nodes = len(G.nodes())
        spring_3D = nx.spring_layout(G, dim=3, seed=18)
        x_nodes = [spring_3D[i][0] for i in range(Num_nodes)]  # x-coordinates of nodes
        y_nodes = [spring_3D[i][1] for i in range(Num_nodes)]  # y-coordinates
        z_nodes = [spring_3D[i][2] for i in range(Num_nodes)]  # z-coordinates
        x_edges = []
        y_edges = []
        z_edges = []

        for edge in G.edges():
            x_coords = [spring_3D[edge[0]][0], spring_3D[edge[1]][0], None]
            x_edges += x_coords

            y_coords = [spring_3D[edge[0]][1], spring_3D[edge[1]][1], None]
            y_edges += y_coords

            z_coords = [spring_3D[edge[0]][2], spring_3D[edge[1]][2], None]
            z_edges += z_coords

        trace_edges = go.Scatter3d(
            x=x_edges,
            y=y_edges,
            z=z_edges,
            mode="lines",
            line=dict(color="black", width=2),
            hoverinfo="none",
        )

        trace_nodes = go.Scatter3d(
            x=x_nodes,
            y=y_nodes,
            z=z_nodes,
            mode="markers",
            marker=dict(
                symbol="circle",
                size=10,
                colorscale=["lightgreen", "magenta"],  # either green or mageneta
                line=dict(color="black", width=0.5),
            ),
            hoverinfo="text",
        )

        axis = dict(
            showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title="",
        )

        layout = go.Layout(
            width=650,
            height=625,
            showlegend=False,
            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
            ),
            margin=dict(t=100),
            hovermode="closest",
        )

        fig = go.Figure(data=[trace_edges, trace_nodes], layout=layout)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, result

    register_algorithms(result, func, wrapper)
    return wrapper


params_algorithms(result, ["matrix"], ext_params={"iframe": True})


@result
def create(G, ax, labels):
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
    colors = [
        "red",
        "blue",
        "green",
        "yellow",
        "black",
        "pink",
        "orange",
        "white",
        "gray",
        "purple",
        "brown",
        "navy",
    ]
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

    return f"Хроматическое число равно {len(set(colors_of_nodes.values()))}."


@result
def dijkstra(G, ax, labels):
    return f"Длина кратчайших путей равена $${sp.latex(nx.shortest_path_length(G, source=0, weight='weight'))}$$\nКратчайшие пути:$${sp.latex(nx.shortest_path(G,source=1,weight='weight'))}$$"
