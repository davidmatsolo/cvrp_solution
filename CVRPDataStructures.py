import random

from matplotlib import pyplot as plt
from DataStructures import Graph

class Vehicle:
    def __init__(self, vehicle_id, capacity):
        self.vehicle_id = vehicle_id
        self.capacity = capacity
        self.load = 0

    def update_load(self, demand):
        self.load += demand

    def check_capacity_constraint(self, demand):
        return self.load + demand <= self.capacity
    
    def get_capacity(self):
        return self.capacity
    

class CVRP:
    def __init__(self, graph_file):
        self.graph = Graph(graph_file)  # Create an instance of the Graph class
        self.vehicles = []
        self.customers = None
        self.customers_demand = None
        self.depot = None
        #print("cvrp created")

        

    def set_depot(self):
        nodes = self.graph.get_nodes()
        
        self.depot = nodes[0]

    def set_customers_demands(self):
        temp_dict = {}
        for i in range(len(self.get_customers())):
            temp_dict[self.get_customers()[i]] = self.graph.get_edge_weights_for_node(self.get_customers()[i])
        
        #print("demands :", temp_dict)
        self.customers_demand = temp_dict

    def get_customers_demands(self):
        return self.customers_demand
        
    def get_customer_demand(self, customer):
        return self.customers_demand[customer]

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def get_graph(self):
        return self.graph

    def get_vehicles(self):
        return self.vehicles

    def get_depot(self):
        return self.depot

    def set_customers(self):
        customers = self.graph.get_nodes()
        customers.remove(self.depot)
        self.customers = customers

    def get_customers(self):
        return self.customers



    def plot_depot_and_customers(self):
        # Get the (x, y) coordinates of the depot and customers
        depot_x, depot_y = random.random() * 10, random.random() * 10  # Random coordinates for the depot
        customer_coords = {}  # Dictionary to store (x, y) coordinates of customers

        for customer in self.get_customers():
            customer_coords[customer] = (random.random() * 10, random.random() * 10)

        # Create a new plot
        plt.figure(figsize=(8, 6))
        plt.scatter(depot_x, depot_y, c='blue', marker='s', s=100, label='Depot')
        
        for customer, coord in customer_coords.items():
            plt.scatter(coord[0], coord[1], c='red', marker='o', s=50, label=f'Customer {customer}')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Depot and Customers Plot')
        plt.legend()
        plt.grid(True)
        plt.show()

