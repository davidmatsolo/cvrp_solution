
import random
from tkinter import messagebox
from PyQt5.QtWidgets import QWidget, QMessageBox
from matplotlib.collections import LineCollection
import networkx as nx
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import matplotlib.pyplot as plt
sys.path.append(r'd:\New folder\pythonProject')  # Add the directory containing pso.py to sys.path


from CVRPDataStructures import CVRP, Vehicle

from gui.pages.problem_window_ui import Ui_Form

from pages_functions.pso import pso_set_cvrp
from pages_functions.bfo import bfo_set_cvrp
from pages_functions.aco import aco_set_cvrp



cvrp_instance = None
file_name = None

def set_filename(new_value):
    global file_name
    file_name = new_value

def get_cvrp_instance():
     return cvrp_instance

class Home(QWidget):
    def __init__(self):
        super(Home, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.generate_problem_btn = self.ui.pushButton

        ## =======================================================================================================
        ## Connect signal and slot
        ## =======================================================================================================
        self.generate_problem_btn.clicked.connect(self.generate_problem)


    def generate_problem(self):
        

        ## =======================================================================================================
        # Create a CVRP instance
        ## =======================================================================================================
        global file_name
        global cvrp_instance
        cvrp_instance = CVRP(file_name)
        

        ## =======================================================================================================
        # Set the depot and customers
        ## =======================================================================================================
        cvrp_instance.set_depot()  # Replace 0 with the index of your depot
        cvrp_instance.set_customers()
        
        
        # Get text from line edits
        num_vehicles_text = self.ui.lineEdit.text()
        vehicle_capacities_text = self.ui.lineEdit_2.text()

        #show inputs
        print("num of vehicles", num_vehicles_text)

        # Check if the input in line edits is valid (you can add more checks as needed)
        if not num_vehicles_text.isdigit() or not vehicle_capacities_text.isdigit():
            # Show an error message
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers for vehicles and capacities.")
        else:
            ## =======================================================================================================
            # Create vehicles and add them to the CVRP instance
            ## =======================================================================================================
            num_vehicles = int(num_vehicles_text)
            vehicle_capacities = int(vehicle_capacities_text)
            for i in range(num_vehicles):
                    print(i)
                    vehicle = Vehicle(i, vehicle_capacities)
                    cvrp_instance.add_vehicle(vehicle)

            ## =======================================================================================================
            # Set customers' demands randomly
            ## =======================================================================================================
            cvrp_instance.set_customers_demands()

            print("problem generated")
            

            ## =======================================================================================================
            #set the cvrp in optimization windows
            ## =======================================================================================================
            pso_set_cvrp(cvrp_instance)
            bfo_set_cvrp(cvrp_instance)
            aco_set_cvrp(cvrp_instance)

            ## =======================================================================================================
            #set the cvrp in optimization windows
            ## =======================================================================================================
            self.plot_graph(cvrp_instance.get_graph(), cvrp_instance.get_depot())


    def plot_graph(self, graph_object, depot):
        graph = graph_object.get_graph()
        pos = graph_object.get_positions()

        # Extract x and y coordinates from the pos dictionary
        x_values = [pos[node]['x'] for node in graph.nodes]
        y_values = [pos[node]['y'] for node in graph.nodes]

        self.ui.convergence_canvas.axes.clear()

        # Create a color map where depot is red and all other nodes are blue
        node_colors = ['red' if node == depot else 'blue' for node in graph.nodes]

        # Plot nodes using extracted x and y coordinates
        pos_dict = {node: (x_values[i], y_values[i]) for i, node in enumerate(graph.nodes)}
        nx.draw_networkx_nodes(graph, pos=nx.spring_layout(graph, pos=pos_dict), node_size=200, node_color=node_colors, ax=self.ui.convergence_canvas.axes)

        # Label nodes with their names
        labels = {node: str(node) for node in graph.nodes}
        nx.draw_networkx_labels(graph, pos=nx.spring_layout(graph, pos=pos_dict), labels=labels, font_color='black', font_size=10, ax=self.ui.convergence_canvas.axes)

        # Set plot limits (you can adjust these)
        self.ui.convergence_canvas.axes.set_xlim(-1.2, 1.2)
        self.ui.convergence_canvas.axes.set_ylim(-1.2, 1.2)

        # Update the canvas
        self.ui.convergence_canvas.draw()


