import copy
import networkx as nx
import random
from CVRPDataStructures import CVRP, Vehicle
from DataStructures import Graph

class Ant:
    def __init__(self, startCity, graph: Graph):
        self.currentCity = startCity
        self.visitedNodes = [startCity]
        self.tourLength = 0.0
        self.graph = graph
        self.position = []
    
        

    def getCurrentCity(self):
        return self.currentCity

    def getVisitedCities(self):
        return self.visitedNodes

    def getTourLength(self):
        return self.tourLength

    def moveToNextCity(self, nextCity):
        if self.graph.has_edge(self.currentCity, nextCity):
            distance = self.graph.get_wights_for_nodes(self.currentCity, nextCity)
        else:
            distance = 1
        self.tourLength += distance
        self.currentCity = nextCity
        self.visitedNodes.append(nextCity)
    
    def add_route(self, route):
        self.lbest_position.append(route)

    def possible_tourLength(self, nextCity):
        temp = self.graph.get_wights_for_nodes(self.currentCity, nextCity)
        posible_length = self.tourLength + temp
        return posible_length
    
    def set_position(self, route):
        self.position.append(route)
    
    def get_position(self):
        return self.position        

    def calculateProbability(self, pheromone_level, heuristic_info, alpha, beta):
        probability = (pheromone_level ** alpha) * (heuristic_info ** beta)
        return probability
    
    def refresh(self, depot):
        self.currentCity = depot
        self.visitedNodes = [depot]
        self.tourLength = 0.0
        self.position = []
        #print("refreshed")
    def reset_tour(self):
        self.tourLength = 0.0




class AntColonyOptimization:
    def __init__(self, problem: CVRP):
        self.graph = problem.get_graph()
        self.problem = problem
        self.vehicles = problem.get_vehicles()
        self.depot = problem.get_depot()
        self.ants = []
        self.pheromoneMatrix = nx.Graph()
        self.heuristicMatrix = nx.Graph()
        self.gbest_position = []
        self.lbest_fitness = float('inf')
        self.gbest_fitness = float('inf')
        self.convergence = []

    def initializePheromoneMatrix(self):
        num_nodes = self.graph.number_of_nodes()
        self.pheromoneMatrix = nx.complete_graph(num_nodes)
        self.pheromoneMatrix = self.pheromoneMatrix.to_directed()
        for u, v in self.pheromoneMatrix.edges:
            self.pheromoneMatrix[u][v]['pheromone'] = random.uniform(0,1)
        
    def initializeHeuristicMatrix(self):
        num_nodes = self.graph.number_of_nodes()
        self.heuristicMatrix = nx.Graph()
        for u, v in self.graph.get_edges():
            distance = self.graph.get_wights_for_nodes(u, v)
            self.heuristicMatrix.add_edge(u, v, weight=random.uniform(0,1) / distance)
        
        
    def initializePopulation(self, num_ants):
        for _ in range(num_ants):
            start_city = self.depot
            ant = Ant(start_city, self.graph)
            self.ants.append(ant)
            


    def is_feasible(self, solution):
        if len(solution) == 0:
            return False
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

        #print("routes ",routes)
        if not self.is_feasible(routes):
            return float('inf')
        else:
            routes_sum = 0
            for v in routes:
                routes_sum += self.routeFitness(v)
                
            routes_fitness = routes_sum / len(routes)

            return  routes_fitness 
        

    def findCycles(self, route):
        start = route[0]
        result = []
        temp = []

        for item in route:
            if item == start:
                if temp:
                    result.append(temp)
                temp = []
            else:
                temp.append(item)

        if temp:
            result.append(temp)

        for sub_array in result:
            sub_array.insert(0, start)
            sub_array.append(start)

        return result



    def updatePheromoneMatrix(self, routes, evaporation_rate):
        delta_pheromone = nx.Graph()

        for route in routes:
            for i in range(len(route) - 1):
                current_city = route[i]
                next_city = route[i + 1]
                if current_city is not None and next_city is not None:
                    if delta_pheromone.has_edge(current_city, next_city):
                        if len(route) != 0.0:
                            delta_pheromone[current_city][next_city]['pheromone'] += 1 / len(route)
                    else:
                        delta_pheromone.add_edge(current_city, next_city, pheromone=0.0)
                        if len(route) != 0.0:
                            delta_pheromone[current_city][next_city]['pheromone'] += 1 / len(route)
                        else:
                            delta_pheromone[current_city][next_city]['pheromone'] += 1

        for u, v in delta_pheromone.edges():
            if self.pheromoneMatrix.has_edge(u, v):
                self.pheromoneMatrix[u][v]['pheromone'] = (
                    (1 - evaporation_rate) * self.pheromoneMatrix[u][v]['pheromone'] +
                    delta_pheromone[u][v]['pheromone']
                )
            else:
                self.pheromoneMatrix.add_edge(u, v, pheromone=delta_pheromone[u][v]['pheromone'])

    def selectNextCity(self, ant, visited_cities, alpha, beta):
        current_city = ant.getCurrentCity()
        probabilities = []

        for next_city in self.graph.get_neighbours(current_city):
            if next_city not in visited_cities or next_city == self.problem.depot:
                pheromone_info = self.pheromoneMatrix.get_edge_data(current_city, next_city)
                if pheromone_info is not None:
                    pheromone_level = pheromone_info['pheromone']
                    heuristic_info = self.heuristicMatrix[current_city][next_city]['weight']
                    probability = ant.calculateProbability(pheromone_level, heuristic_info, alpha, beta)
                    probabilities.append((next_city, probability))

        if not probabilities:
            unvisited_cities = [city for city in self.graph.get_nodes() if city not in visited_cities]
            return random.choice(unvisited_cities)

        total_probability = sum(prob for _, prob in probabilities)
        if total_probability != 0.0:
            probabilities = [(city, prob / total_probability) for city, prob in probabilities]
        else:
            probabilities = [(city, 1.0 / len(probabilities)) for city, _ in probabilities]
    
        selected_city = self.selectByProbability(probabilities)

        if selected_city == self.problem.depot and visited_cities.count(self.problem.depot) == 1:
            # Choose another city instead of the first depot
            unvisited_cities = [city for city in self.graph.get_nodes() if city not in visited_cities]
            #print("unvisited", unvisited_cities)
            if self.problem.get_depot() in unvisited_cities:
                unvisited_cities.remove(self.problem.get_depot())
            return random.choice(unvisited_cities)

        return selected_city


    def selectByProbability(self, probabilities):
        random_value = random.random()
        cumulative_probability = 0.0
        for city, probability in probabilities:
            cumulative_probability += probability
            if random_value <= cumulative_probability:
                return city

        # If no city is selected, choose a random city (fallback)

        return random.choice(probabilities)[0]
    

    def constructSolution(self, num_ants, iterations, evaporation_rate, alpha, beta):
        self.initializePopulation(num_ants)
        num_nodes = len(self.problem.get_customers())
        self.capacity = self.vehicles[0].get_capacity()
        
        max_iterations = 0
        previous_best = None

        while max_iterations < iterations:
            #print()
            #print("iteration : ", (max_iterations+1))
            i =1
            for ant in self.ants:
                
                available_vehicles = len(self.problem.get_vehicles())
                #print("vehicles", available_vehicles)
                generated_route = [self.depot]
                visited_cities = set()
                ant_visited_cities = [ant.getCurrentCity()]
                #print("initial current is ", ant.getCurrentCity())
                visited_cities.add(ant.getCurrentCity())
                #print("ant ",  i , " visited cities are ", visited_cities)
                i+=1


                #construct local solution 
                while len(ant_visited_cities) < (num_nodes):
                    next_city = self.selectNextCity(ant, ant_visited_cities, alpha, beta)
                    if(next_city == self.depot):
                        print("we selected depot")
                    
                    if available_vehicles ==1:
                        #print("im here now")
                        all_cities = copy.deepcopy(set(self.graph.get_nodes()))
                        visited_cities.add(next_city)
                        missing_cities = all_cities.difference(visited_cities)
                        #print("I have generate {} and I visited this:  {}".format(generated_route, visited_cities))

                        generated_route = [self.depot]
                        generated_route.append(next_city)
                        

                        while len(missing_cities) > 0:
                            random_city = random.choice(list(missing_cities))
                            missing_cities.remove(random_city)
                            generated_route.append(random_city)

                        generated_route.append(self.depot)
                        ant.set_position(generated_route)
                        #print("ant found ", ant.get_position() )
                        #print()
                        break


                    else:
                        if ant.possible_tourLength(next_city) <= self.capacity:
                            ant.moveToNextCity(next_city)
                            ant_visited_cities.append(next_city)
                            visited_cities.add(next_city)
                            generated_route.append(next_city)
                        else:
                        
                            #print("test " ,ant.possible_tourLength(next_city))
                            #save the old route
                            generated_route.append(self.depot)
                            #save it as a valid route among positions
                            ant.set_position(generated_route)

                            
                            #create a new route
                            generated_route = [self.depot]
                            ant.reset_tour()
                            ant.moveToNextCity(next_city)
                            generated_route.append(next_city)
                            available_vehicles -= 1
                            ant_visited_cities.append(next_city)
                            
                            

                    

                

            for ant in self.ants:
                localfitness = self.routes_fitness(ant.get_position())
                if localfitness < self.gbest_fitness:
                    self.gbest_fitness = localfitness
                    self.gbest_position = ant.get_position()
                
            self.convergence.append(self.gbest_fitness)
            self.updatePheromoneMatrix(self.gbest_position, evaporation_rate)

            if previous_best is None:
                previous_best = self.gbest_position
            else:
                if self.gbest_position == previous_best:
                    max_iterations += 1
                else:
                    max_iterations = 0
            previous_best = self.gbest_position

            for ant in self.ants:
                ant.refresh(self.depot)
            


        return self.gbest_position, self.gbest_fitness, self.convergence




"""
# Replace 'your_graph_file.csv' with the actual path to your graph file
graph_file = 'simplified_graph.txt'
problem = CVRP(graph_file)

# Set the depot and customers
problem.set_depot()  # Replace 0 with the index of your depot
problem.set_customers()

# Create vehicles and add them to the CVRP instance
num_vehicles = 2 # Replace with the number of vehicles you want
vehicle_capacities = [18,18]  # Replace with the capacities of your vehicles
for i in range(num_vehicles):
    vehicle = Vehicle(vehicle_id=i, capacity=vehicle_capacities[i])
    problem.add_vehicle(vehicle)

# Set customers' demands randomly
problem.set_customers_demands()

aco = AntColonyOptimization(problem)

num_ants = 134  # Number of ants
iterations = 123  # Number of iterations


aco.initializePheromoneMatrix()
aco.initializeHeuristicMatrix()

position, fitness, convergence = aco.constructSolution(num_ants, iterations, 0.38, 0.71, 0.04)

print()
print("position", position)
print("fitness ", fitness)
print("convergence ", convergence)
print(type(convergence[0]))
"""