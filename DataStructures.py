import itertools
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx


class Graph:
    def __init__(self, file_name):
        self.file_name = file_name
        self.graph = nx.Graph()
        self.nodes_locations = {}
        self._read_graph_from_file()
        

    def _read_graph_from_file(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                node, x_coordinate, y_coordinate = map(int, line.strip().split(','))  # Assume edges are separated by commas
                self.nodes_locations[node] = (x_coordinate, y_coordinate)
                
                self.graph.add_node(node, x=x_coordinate, y=y_coordinate)
        
        self.set_edge_weights_based_on_coordinates()

    def get_graph(self):
        return self.graph

    def number_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_nodes(self):
        return list(self.graph.nodes)

    def get_edges(self):
        return self.graph.edges

    def get_edge_data(self, source, destination):
        return self.graph.get_edge_data(source, destination)

    def has_edge(self, source, destination):
        return self.graph.has_edge(source, destination)
    

    def get_edge_weights_for_node(self, node):
        edge_weights = {}
        for neighbor in self.graph.neighbors(node):
            edge_data = self.graph.get_edge_data(node, neighbor)
            if edge_data:
                edge_weights[neighbor] = edge_data['weight']
        return edge_weights

    def get_wights_for_nodes(self, node1, node2):
        return self.graph[node1][node2]['weight']
    
    def get_neighbours(self, node):
        return self.graph.neighbors(node)
    
    def set_edge_weights_based_on_coordinates(self):
        for node1, node2 in itertools.combinations(self.graph.nodes, 2):
            x1, y1 = self.nodes_locations[node1]
            x2, y2 = self.nodes_locations[node2]
            distance = int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)
            self.graph.add_edge(node1,node2,weight = distance)
        

    def get_positions(self):
        return self.graph.nodes(data=True)




"""
def plot_graph(graph_object):
    graph = graph_object.get_graph()
    pos = graph_object.get_positions()

    # Create a figure and axis
    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # Extract x and y coordinates from the pos dictionary
    x_values = [pos[node]['x'] for node in graph.nodes]
    y_values = [pos[node]['y'] for node in graph.nodes]

    # Plot nodes using extracted x and y coordinates
    nx.draw_networkx_nodes(graph, pos={node: (x_values[i], y_values[i]) for i, node in enumerate(graph.nodes)}, node_size=200, ax=ax)

    # Label nodes with their names
    labels = {node: str(node) for node in graph.nodes}
    nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph), labels=labels, font_size=10,font_color='black', ax=ax)

    #plt.axis('off')  # Turn off axis labels
    print("Nodes in plot : ", graph.nodes)
    # Show the plot
    plt.show()

def main():
    # Create a Graph object by providing the file name
    graph = Graph('graph.txt')  # Replace 'your_graph_data.txt' with the actual file name

    # Perform operations on the graph
    print("Number of nodes:", graph.number_of_nodes())
    print("Nodes:", graph.get_nodes())
    # print("Edges:", graph.get_edges())

    #for u, v in graph.get_edges():
    #    weight = graph.get_wights_for_nodes(u, v)
    #    print(f"Weight of edge ({u}, {v}): {weight}")

    # Plot the graph
    plot_graph(graph)

if __name__ == "__main__":
    main()
"""