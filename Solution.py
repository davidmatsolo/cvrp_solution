class Solution:
    def __init__(self):
        self.vehicle_assignments = {}
        self.fitness = float('inf')

    def assign_route_to_vehicle(self, vehicle, route):
        self.vehicle_assignments[vehicle] = route 

    def get_routes(self):
        return [route for routes in self.vehicle_assignments.values() for route in routes]

    def get_vehicle_assignments(self):
        return self.vehicle_assignments

    def get_vehicles(self):
        return list(self.vehicle_assignments.keys())
    
    def set_fitness(self, fitness):
        self.fitness = fitness 
   
    def get_fitness(self):
        return self.fitness  

    def copy(self):
        copied_solution = Solution()
        copied_solution.vehicle_assignments = {k: v[:] for k, v in self.vehicle_assignments.items()}
        return copied_solution
