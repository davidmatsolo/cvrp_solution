from itertools import chain
import random
import copy
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import numpy as np

from CVRPDataStructures import CVRP, Vehicle
from Solution import Solution
import networkx as nx



class Bacterium:
    def __init__(self, depot,vehicle_capacity, customers , customers_demands, graph,vehicles):
        self.customers = customers
        self.depot_location = depot
        self.vehicle_capacity = vehicle_capacity
        self.customers_demands = customers_demands
        self.graph = graph
        self.vehicles = vehicles
        self.step_size = random.uniform(1,2)
        self.num_vehicles = len(vehicles)
        self.position = self._initialize_position()
        self.bacterium_best_position = self.position[:]
        self.bacterium_best_fitness = float('inf')


    def _initialize_position(self):
        positions =None
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
        #print("positions ", positions)
        return positions

    def set_position(self, position):
        self.position = position
        self.bacterium_best_position = position[:]
    
    def get_position(self):
        return self.position
    
    def reset_fitness(self):
        self.bacterium_best_fitness = float('inf')
    
    def is_feasible(self, routes):
        for solution in routes:
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


        return total

    
    def routes_fitness(self, routes):

        if not self.is_feasible(routes):
            return float('inf') , 89 
        else:
            routes_sum = 0
            for v in routes:
                routes_sum += self.routeFitness(v)

            routes_fitness = routes_sum / len(routes)

        return routes_fitness, routes_sum



    def evaluate_fitness(self):
        def is_equal_lists(a, b):
            return all(a[i] == b[i] for i in range(len(a)))

        # Implementing a function to calculate the total distance/cost of all routes
        # representing by self.position, considering the vehicle capacity constraints.
        # Update self.pbest_fitness and self.pbest_position accordingly.
        temp_position = list(chain.from_iterable(self.position))
        position = list(filter(lambda x: x != self.depot_location, temp_position))


        if is_equal_lists(np.sort(position), np.sort(self.customers)):
            fitness, total_demand = self.routes_fitness(self.position)
            
        
            if fitness <= self.bacterium_best_fitness:
                self.bacterium_best_fitness = fitness
                self.bacterium_best_position = self.position
    
    def chemotaxis(self, c, Ns, gbest_position, gbest_fitness):
        
        for _ in range(Ns):
            
            # Update step size using Eq. (3)
            # Tumble: Generate step in each dimension
            self.step_size = self.step_size * random.uniform(c, (c * np.exp(-gbest_fitness)))

            # Compute new position using Eq. (4)
            #swim to new position
            self.update_position(gbest_position)
            
            # Evaluate fitness of the new position
            self.evaluate_fitness()
         
            
    

    def update_position(self,gbest_position):

        remaining_customers = copy.deepcopy(self.customers)
        l = random.random()
        r1,r2 = 0.5, 1.3

        

        def find_closest_integer(double_value, array):
            closest = array[0]

            for num in array:
                if abs(num - double_value) < abs(closest - double_value):
                    closest = num
            return closest

        def list_from_solution(routes):
           
            positions = list(chain.from_iterable(routes))
            generated_route = list(filter(lambda x: x != self.depot_location, positions))
            
            return generated_route

        
        bposition = list_from_solution(self.position)
        lbest = list_from_solution(self.bacterium_best_position)
        gbest = list_from_solution(gbest_position)

        # Compute the distance vector towards the global best position
        distance_vector = [(gbest[i] - bposition[i]) for i in range(len(bposition))]


        new_routes = []

        # Compute new position using Eq. (4)
        # Swim: Move in the direction of the step size
        for i in range(len(bposition)):
                #swim from current position to nearest global best position
                first_part = l * r1 * (lbest[i] - bposition[i])
                second_part = (1-l) * r2 * (gbest[i]-bposition[i])
                new_position = bposition[i] + (self.step_size*distance_vector[i]) + first_part + second_part
                chosen_customer = find_closest_integer(new_position, remaining_customers)
                new_routes.append(chosen_customer)
                remaining_customers.remove(chosen_customer)
        

        for v in range(len(self.position)):
            route_length = len(self.position[v])-1
            for i in range(1, route_length):
                self.position[v][i] = new_routes.pop(0)    
        

    def get_bacterium_fitness(self):
         return self.bacterium_best_fitness
    
    def get_bacterium_best_position(self):
         return self.bacterium_best_position




class BFO:
    def __init__(self, cvrp_instance, population_size, num_iterations):
        self.cvrp_instance = cvrp_instance
        self.population_size = population_size
        self.num_iterations = num_iterations
        self.colony = self._initialize_colony()
        self.gbest_position = None
        self.gbest_fitness = float('inf')
        self.convergence = []  # List to store the convergence data

    def _initialize_colony(self):
            bacterial_depot = self.cvrp_instance.get_depot()
            bacterial_customers = self.cvrp_instance.get_customers()
            bacterial_customers_demands = self.cvrp_instance.get_customers_demands()
            bacterial_graph = self.cvrp_instance.get_graph()
            bacterial_vehicles = self.cvrp_instance.get_vehicles()

            swarm = [Bacterium(bacterial_depot,
                         bacterial_vehicles[0].get_capacity(),
                         bacterial_customers,
                         bacterial_customers_demands,
                         bacterial_graph,
                         bacterial_vehicles)
                    for _ in range(self.population_size)]
        
            return swarm


    def reproduction(self):
        # Sort bacteria based on their health status (lifetime fitness)
        self.colony.sort(key=lambda b: b.get_bacterium_fitness(), reverse=True)
        
        # Select the first half of the population (surviving bacteria)
        surviving_population = self.colony[:self.population_size // 2]

        # Create offspring by copying each surviving bacterium
        offsprings = []
        for parent in surviving_population:
            # Create two identical offspring with the same position and step size as the parent
            child = copy.deepcopy(parent)
            child.set_position(parent.get_position())
            child.reset_fitness()
            offsprings.append(child)
            
        # Replace the existing population with the offspring
        #self.colony = surviving_population
        self.colony.extend(offsprings)


    def elimination_dispersal(self, Ped):
        # Sort bacteria based on their health status (lifetime fitness)
        self.colony.sort(key=lambda b: b.get_bacterium_fitness())

        # Compute the number of bacteria to eliminate based on Ped
        num_to_eliminate = int(Ped * self.population_size)


        # Eliminate the worst bacteria (num_to_eliminate) from the colony
        self.colony = self.colony[:-num_to_eliminate]

        # Repopulate the colony with new bacteria
        new_bacteria = [Bacterium(
            self.cvrp_instance.get_depot(),
            self.cvrp_instance.get_vehicles()[0].get_capacity(),
            self.cvrp_instance.get_customers(),
            self.cvrp_instance.get_customers_demands(),
            self.cvrp_instance.get_graph(),
            self.cvrp_instance.get_vehicles()
        ) for _ in range(num_to_eliminate)]
        
        for agent in new_bacteria:
            agent.evaluate_fitness()
            #print("new bacteria", agent.get_bacterium_best_position(), "with fitness ", agent.get_bacterium_fitness())

        self.colony.extend(new_bacteria)


        
    def constructSolution(self, Nc, Ns, Nre,  Ped, Cmax, Cmin):
            max_iterations = 0
            previous_best = None
            
            while max_iterations < self.num_iterations:
                #print("iteration", iteration+1)
                
                a = 1.7  # Adjustable coefficient for the step size
                n = 2  # Modulation index

                Cj = Cmin + np.exp(-a * ((self.num_iterations+1) / Nre) ** n) * (Cmax - Cmin) #step size
                #print("gbest position ", self.gbest_position)
                #perform chemotaxis and reproduction for each bacterium
                for bacterium in self.colony:
                    if bacterium.get_bacterium_fitness() < self.gbest_fitness:
                            bacterium.evaluate_fitness()
                            self.gbest_fitness = bacterium.get_bacterium_fitness()
                            self.gbest_position = bacterium.get_bacterium_best_position()
                            

                            #Nc chemotaxis steps
                            for _ in range(Nc):
                                bacterium.chemotaxis(Cj,Ns,self.gbest_position, self.gbest_fitness)
                
                          
                #reproduce
                self.reproduction() 

                #eliminate bad bacteria in colony
                self.elimination_dispersal(Ped)
                
                #update convegence array
                self.convergence.append(self.gbest_fitness)
                #print("gbest position ", self.gbest_position)

                if previous_best is None:
                    previous_best = self.gbest_position
                else:
                    if self.gbest_position == previous_best:
                        max_iterations += 1
                    else:
                        max_iterations = 0
                previous_best = self.gbest_position

            
            
            
                 
            
            
            return self.gbest_position, self.gbest_fitness, self.convergence
            
                

"""
# Create a CVRP instance
cvrp_instance = CVRP("simplified_graph.txt")

# Set the depot and customers
cvrp_instance.set_depot()  # Replace 0 with the index of your depot
cvrp_instance.set_customers()

# Create vehicles and add them to the CVRP instance
num_vehicles = 2  # Replace with the number of vehicles you want
vehicle_capacities = [18,18]  # Replace with the capacities of your vehicles
for i in range(num_vehicles):
    vehicle = Vehicle(vehicle_id=i, capacity=vehicle_capacities[i])
    cvrp_instance.add_vehicle(vehicle)

# Set customers' demands randomly
cvrp_instance.set_customers_demands()

bfo = BFO(cvrp_instance, 25,400)
position, fitness, convergence = bfo.constructSolution(5,50,10,0.4,0.1,0.01)
print()
print("initial solution", type(convergence[0]))
print(convergence)
print("position", position)
"""
