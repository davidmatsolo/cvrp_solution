from copy import deepcopy
import random
from PyQt5.QtWidgets import QWidget, QMessageBox
from matplotlib.collections import LineCollection
import networkx as nx
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib.pyplot as plt
sys.path.append(r'd:\New folder\pythonProject')  
import time

from CVRPDataStructures import CVRP, Vehicle
from ACO import AntColonyOptimization
from gui.pages.aco_window_ui import Ui_Form


## =======================================================================================================
## create global  objects
## =======================================================================================================
aco_cvrp = None

def aco_set_cvrp(cvrp):
    global aco_cvrp
    aco_cvrp = cvrp

def get_aco_cvrp():
    return aco_cvrp


class ACO_WINDOW(QWidget):
    def __init__(self):
        super(ACO_WINDOW, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        ## =======================================================================================================
        ## Get all the objects in windows
        ## =======================================================================================================
        self.solve_aco_btn = self.ui.pushButton
        self.cvrp_instance = None


        ## =======================================================================================================
        ## Connect signal and slot
        ## =======================================================================================================
        
        self.solve_aco_btn.clicked.connect(self.solve_with_aco)

    
    def solve_with_aco(self):

        lineEdits = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.lineEdit_6.text(),
        ]

        if any(not text for text in lineEdits):
            # At least one lineEdit is empty, show an error message
            QMessageBox.critical(self, "Error", "Please fill in all the fields.")
            return

        population = int(self.ui.lineEdit.text()) #45
        iterations = int(self.ui.lineEdit_2.text()) #78
        rate = float(self.ui.lineEdit_3.text()) #0.8
        alpha = float(self.ui.lineEdit_4.text())#0.1
        beta = float(self.ui.lineEdit_6.text())#0.04

        print(population)

        self.cvrp_instance = get_aco_cvrp()
        print("vehicles ", len(self.cvrp_instance.get_vehicles()))

        """
        # assign a CVRP instance
        if self.cvrp_instance is None:
            # If self.cvrp_instance is not set, set it
            self.cvrp_instance = get_aco_cvrp()
        else:
            print("customer in aco ", self.cvrp_instance.get_customers())
        """
        

        ## =======================================================================================================
        # Create the ACO object and run the algorithm
        ## =======================================================================================================
        aco_algo = AntColonyOptimization(self.cvrp_instance)

        aco_algo.initializePheromoneMatrix()
        aco_algo.initializeHeuristicMatrix()

        start_time = time.time()
        print("start time", start_time)

        self.position, self.fitness, self.convergence = aco_algo.constructSolution(population,iterations, rate, alpha, beta)
        #position, fitness,convergence = pso.run(w=0.16, c1=1.695, c2=1.5)

        finish_time = time.time()
        print("finish time", finish_time)

        print()
        elapsed_time = finish_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        print()



        print("gbest: ", self.position)
        print("fitness :", self.fitness)
        print("convergence :", self.convergence)
        
        ## =======================================================================================================
        ## Show the solution
        ## =======================================================================================================
        self.plotconvergence(self.convergence)
        self.plot_solution(self.position)
        
        

    def plotconvergence(self, convergence_array):

        n_data = len(convergence_array)
        self.xdata = list(range(n_data))
        self.ydata = convergence_array
        self.update_plot()

        #self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.ui.convergence_canvas.axes.cla()  # Clear the canvas.
        self.ui.convergence_canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.ui.convergence_canvas.draw()
        

    def plot_solution(self, solution):
        # Create a graph
        G = self.cvrp_instance.get_graph().get_graph()
        pos = self.cvrp_instance.get_graph().get_positions()
        depot = self.cvrp_instance.get_depot()

        # Extract x and y coordinates from the pos dictionary
        x_values = [pos[node]['x'] for node in G.nodes]
        y_values = [pos[node]['y'] for node in G.nodes]

        
        # Add edges based on the given routes
        print("solutions : ", solution)
        routes = solution #[[1, 2, 4, 6, 1], [1, 3, 5, 7, 1]]  # Example routes

        # Generate random edge colors for each route
        edge_colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in routes]

        # Clear the canvas
        self.ui.graph_canvas.axes.clear()

        # Create a color map where depot is red and all other nodes are blue
        node_colors = ['red' if node == depot else 'blue' for node in G.nodes]

        # Draw the nodes
        pos_dict = {node: (x_values[i], y_values[i]) for i, node in enumerate(G.nodes)}
        nx.draw_networkx_nodes(G, pos=nx.spring_layout(G, pos=pos_dict), node_size=200, node_color=node_colors, ax=self.ui.graph_canvas.axes)

        # Draw the edges with different colors for each route
        for route, color in zip(routes, edge_colors):
            edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            nx.draw_networkx_edges(G, pos= nx.spring_layout(G, pos=pos_dict), edgelist=edges, edge_color=color, width=2, ax=self.ui.graph_canvas.axes)

        # Draw node labels
        labels = {node: str(node) for node in G.nodes}
        nx.draw_networkx_labels(G, pos=nx.spring_layout(G, pos=pos_dict), font_size=12, font_color='black', ax=self.ui.graph_canvas.axes)

        # Set plot limits (you can adjust these)
        self.ui.graph_canvas.axes.set_xlim(-1.2, 1.2)
        self.ui.graph_canvas.axes.set_ylim(-1.2, 1.2)

        # Update the canvas
        self.ui.graph_canvas.draw()



