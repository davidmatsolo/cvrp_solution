import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

point_to_show = 3
my_list = np.array([12.5, 12.5, 12.5, 12.5, 12.5, 11.0, 11.0, 11.0, 11.0, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.5, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0])

fig, ax = plt.subplots()
line, = ax.plot(range(point_to_show), np.zeros(point_to_show) * np.NaN, 'ro-')
ax.set_ylim(0, 15)  # Adjusted the y-axis limit to better fit the data range
ax.set_xlim(0, point_to_show - 1)

def update(i):
    new_data = my_list[i:i + point_to_show]
    line.set_ydata(new_data)
    ax.set_xlim(i, i + point_to_show - 1)  # Adjusted the x-axis limit based on the current frame
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(my_list) - point_to_show + 1, interval=500)
plt.show()


"""        
    def open_file(self):
        
        global cvrp_instance
        global pso

        #local viriacle
        file_name, _ = QFileDialog.getOpenFileName()
        
        if file_name:
            # You can perform any further processing with the selected file here
            file_name_only = os.path.basename(file_name)
            
        cvrp_instance = CVRP(file_name_only)
        
        # Set the depot and customers
        cvrp_instance.set_depot(depot=1)  # Replace 0 with the index of your depot
        cvrp_instance.set_customers()

        # Create vehicles and add them to the CVRP instance
        num_vehicles = 2  # Replace with the number of vehicles you want
        vehicle_capacities = [10, 15]  # Replace with the capacities of your vehicles
        for i in range(num_vehicles):
            vehicle = Vehicle(vehicle_id=i, capacity=vehicle_capacities[i])
            cvrp_instance.add_vehicle(vehicle)

        # Set customers' demands randomly
        cvrp_instance.set_customers_demands()

        cvrp_instance.plot_depot_and_customers()


    def show_pso_convergence(self):
        global pso
        global cvrp_instance

        #plotter = Plotter() 
        #initialize the algorithms using the generated capacitated vvehicle routing problem
        pso = PSO(num_particles=13, max_iterations=30, cvrp_instance=cvrp_instance)


        _, _, convergence = pso.run(w=0.16, c1=1.695, c2=1.5)

        print("convergence", convergence)


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


    def solve_PSO(self):
        pass
"""
