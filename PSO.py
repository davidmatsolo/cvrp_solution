import copy
import random
from itertools import chain
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import sort

from CVRPDataStructures import CVRP, Vehicle
from DataStructures import Graph
#from Plotter import Plotter



class Particle:
    def __init__(self, depot, vehicle_capacity, customers, customers_demands, graph, vehicles):

        self.customers = customers
        self.depot_location = depot
        self.vehicle_capacity = vehicle_capacity
        self.customers_demands = customers_demands
        self.graph = graph
        self.num_vehicles = len(vehicles)
        self.position = self._initialize_position()
        self.velocity = self._initialize_velocity()
        self.pbest_position = self.position[:]
        self.pbest_fitness = float('inf')


    def _initialize_position(self):
        positions = [[self.depot_location] for _ in range(self.num_vehicles)]
        remaining_customers = copy.deepcopy(self.customers)
        total_demand =0

        for v in range(self.num_vehicles):
            while True: 
                if not remaining_customers:
                    break
                    
                customer = random.choice(remaining_customers)
                tail = positions[v][-1]
                tail_demand = self.graph.get_edge_data(customer, tail)['weight']
                depot_demand = self.graph.get_edge_data(customer, self.depot_location)['weight']

                
                if len(positions[v]) ==1: 
                    #print("depot data :", depot_demand)
                    total_demand = 2 * depot_demand
                else:
                    total_demand = total_demand + tail_demand 

                #
                #print("total demand ",total_demand)
                if total_demand <= self.vehicle_capacity:
                    #print("customer ", customer)
                    positions[v].append(customer)
                    remaining_customers.remove(customer)
                else:
                    break  # Move to the next vehicle
        
        if not remaining_customers:
            pass
        else:
            positions[-1].extend(remaining_customers)

        for v in range(self.num_vehicles):
            positions[v].append(self.depot_location)

        #print("particle positions", positions)
        
        return positions
        

                    


    def _initialize_velocity(self):
        velocity = [[] for _ in range(self.num_vehicles)]

        for v in range(self.num_vehicles):
            route_length = len(self.position[v])
            velocity[v] = [random.uniform(-1, 1) for _ in range(1, route_length - 1)]
            
        return velocity
    def is_equal_lists(self,a, b):
        return all(a[i] == b[i] for i in range(len(a)))

    
    def update_velocity(self, w, c1, c2, gbest_position):
        r1, r2 = random.uniform(0, 1), random.uniform(0, 1)

        temp_customers = list(chain.from_iterable(gbest_position))
        positions = list(chain.from_iterable(self.position))
        pbest_customers = list(chain.from_iterable(self.position))
       

        gbest_customers = list(filter(lambda x: x != 1, temp_customers))
        positions = list(filter(lambda x: x != 1, positions))
        pbest_customers = list(filter(lambda x: x != 1, pbest_customers))

        sorted_gbest_customers = sort(gbest_customers)
        sorted_customers = sort(self.customers)
    
        
        for i in range(len(gbest_customers)):
                
            if self.is_equal_lists(sorted_gbest_customers,sorted_customers) == True:
                cognitive = c1 * r1 * (pbest_customers[i] - positions[i])
                social = c2 * r2 * (gbest_customers[i] - positions[i])
                #random_component = random.uniform(0, 1)
                for v in range(len(self.velocity)):
                    route_length = len(self.velocity[v]) - 1
                    for j in range(1, route_length-1):
                        self.velocity[v][j] = (w * self.velocity[v][j]) + cognitive + social # random_component
        
    def update_position(self):
        remaining_customers = copy.deepcopy(self.customers)
        
        def find_closest_integer(double_value, array):
            closest = array[0]

            for num in array:
                if abs(num - double_value) < abs(closest - double_value):
                    closest = num
            return closest



        for v in range(self.num_vehicles):
            route_length = len(self.velocity[v]) 
            for i in range(route_length):
                double_postion = self.position[v][i+1] + self.velocity[v][i]
                picked_customer = find_closest_integer(double_postion, remaining_customers)
                self.position[v][i+1] = picked_customer

                remaining_customers.remove(picked_customer)
                
    def is_feasible(self, solution):
        for i in range(len(solution) - 1):
            if solution[i] == solution[i + 1]:
                return False
        return True
    
    def routeFitness(self, route):
        demand = 0
        total = 0

        for i in range(1, len(route)):
            prev = route[i - 1]
            current = route[i]

            if current == prev:
                pass
            else:
                demand = self.graph.get_edge_data(prev, current)['weight']
                total += demand

        if total > self.vehicle_capacity:
            return float('inf')

        return total
    
    def routes_fitness(self, routes):

        if not self.is_feasible(routes):
            return routes, float('inf')
        else:
            routes_sum = 0
            for v in routes:
                routes_sum += self.routeFitness(v)
                
            routes_fitness = routes_sum / len(routes)

            return  routes_fitness, routes



    def evaluate_particle_fitness(self):
        # Implementing a function to calculate the total distance/cost of all routes
        # representing by self.position, considering the vehicle capacity constraints.
        # Update self.pbest_fitness and self.pbest_position accordingly.
        temp_position = list(chain.from_iterable(self.position))
        position = list(filter(lambda x: x != 1, temp_position))
             
        if self.is_equal_lists(sort(position), sort(self.customers)):
            fitness, total_demand = self.routes_fitness(self.position)
            if fitness < self.pbest_fitness:
                self.pbest_fitness = fitness
                self.pbest_position = self.position

    def get_pbest_position(self):
        return self.pbest_position
    
    def get_pbest_fitness(self):
        return self.pbest_fitness
        

class PSO:
    def __init__(self, num_particles, max_iterations, cvrp_instance):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.cvrp_instance = cvrp_instance
        self.swarm = self._initialize_swarm()
        self.gbest_position = None
        self.gbest_fitness = float('inf')
        self.convergence = []  # Initialize the convergence list.

    def _initialize_swarm(self):
        particle_depot = self.cvrp_instance.get_depot()
        particle_customers = self.cvrp_instance.get_customers()
        particle_customers_demands = self.cvrp_instance.get_customers_demands()
        particle_graph = self.cvrp_instance.get_graph()
        particle_vehicles = self.cvrp_instance.get_vehicles()

        swarm = [Particle(particle_depot,
                         particle_vehicles[0].get_capacity(),
                         particle_customers,
                         particle_customers_demands,
                         particle_graph,
                         particle_vehicles)
                for _ in range(self.num_particles)]
        
        return swarm
    

    def constructSolution(self, w, c1, c2):

        

        #print()
        for iteration in range(self.max_iterations):
            for particle in self.swarm:
                particle.evaluate_particle_fitness()
                #print(particle.get_pbest_fitness())
                
                if (particle.get_pbest_fitness() < self.gbest_fitness):
                    self.gbest_fitness = particle.get_pbest_fitness()
                    self.gbest_position = particle.get_pbest_position()
            
            
            for particle in self.swarm:
                particle.update_velocity(w, c1, c2, self.gbest_position) 
                particle.update_position()
                
            self.convergence.append(self.gbest_fitness)
            #print("gbest", self.gbest_position)
        return self.gbest_position, self.gbest_fitness, self.convergence



"""

# Create a CVRP instance
cvrp_instance = CVRP("graph.txt")

# Set the depot and customers
cvrp_instance.set_depot(depot=1)  # Replace 0 with the index of your depot
cvrp_instance.set_customers()

# Create vehicles and add them to the CVRP instance
num_vehicles = 2  # Replace with the number of vehicles you want
vehicle_capacities = [23, 23]  # Replace with the capacities of your vehicles
for i in range(num_vehicles):
    vehicle = Vehicle(vehicle_id=i, capacity=vehicle_capacities[i])
    cvrp_instance.add_vehicle(vehicle)

# Set customers' demands randomly
cvrp_instance.set_customers_demands()



# Create the PSO object and run the algorithm
pso = PSO(num_particles=267, max_iterations=30, cvrp_instance=cvrp_instance)
#position, fitness,convergence = pso.run(w=0.0886, c1=0.8795, c2=0.455)
position, fitness,convergence = pso.constructSolution(w=0.6, c1=0.1, c2=0.02)

print("gbest: ", position)
print("fitness :", fitness)
print("convergence :", convergence)


def update(frame):
            plt.cla()  # Clear the current axes

            # Update data for the graph
            x = range(frame+1)
            y = convergence[:frame+1]

            # Plot the graph
            plt.plot(x, y, marker='o', linestyle='-', color='b')
            plt.xlabel('Iterations')
            plt.ylabel('Convergence')
            plt.title('Convergence Over Time')

            # Set the y-axis limits to accommodate the data range
            plt.ylim(min(convergence) - 1, max(convergence) + 1)

            # Annotate the last value
            plt.annotate(f'{y[-1]:.1f}', (x[-1], y[-1]), textcoords="offset points", xytext=(-8,0), ha='right')

# Set up the figure and axis
fig, ax = plt.subplots()

        # Create the FuncAnimation object
ani = FuncAnimation(fig, update, frames=len(convergence), interval=10, repeat=False)

plt.show()

import networkx as nx
import matplotlib.pyplot as plt
import random

# Create a graph
G = nx.Graph()

# Add nodes
nodes = cvrp_instance.get_customers()
G.add_nodes_from(nodes)

# Add edges based on the given routes
routes = position

# Generate random edge colors in hexadecimal format for each route
edge_colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in routes]

all_edges = []  # Accumulate all edges for all routes

for idx, route in enumerate(routes):
    edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    all_edges.extend(edges)  # Accumulate edges
    for i in range(len(route) - 1):
        G.add_edge(route[i], route[i + 1], color=edge_colors[idx])  # Assign edge color

# Create a layout for the nodes
pos = nx.spring_layout(G)

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=500)

# Draw all the accumulated edges with different colors for each route
for idx, color in enumerate(edge_colors):
    route_edges = [edge for edge in all_edges if G.edges[edge]['color'] == color]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color=color, width=2.0)

# Draw node labels
nx.draw_networkx_labels(G, pos)

# Set plot title
plt.title("Vehicle Routing Problem Routes with Random Hex Edge Colors")

# Show the plot
plt.show()

"""


