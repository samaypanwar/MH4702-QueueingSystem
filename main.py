import pandas as pd
from simulation import SimulationStuff

# simulation = SimulationStuff()
# results = pd.DataFrame()

# while simulation.time < 100:
#     print(f"Current time is {simulation.time}.")
#     simulation.time_step()
#     stats = simulation.calculate_stats()
#     print(f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}.")

# print("\nSimulation complete.")
# print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")

def run_simulation(arrival_lambda, bus_seats, bus_stops):
    simulation = SimulationStuff(arrival_lambda, bus_seats, bus_stops)

    while simulation.time < 100:
        print(f"Current time is {simulation.time}.")
        simulation.time_step()
        stats = simulation.calculate_stats()
        print(f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}.")

    print("\nSimulation complete.")
    print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")

    return {
        'arrival_lambda': arrival_lambda,
        'bus_seats': bus_seats,
        'bus_stops': bus_stops,
        'arrivals': simulation.total_arrivals,
        'served': simulation.total_served
    }

results = []
for arrival_lambda in [5, 10, 15]:
    for bus_seats in [10, 20, 30, 40]:
        for bus_stops in [5, 10, 15]:
            results.append(run_simulation(arrival_lambda, bus_seats, bus_stops))
results_df = pd.DataFrame(results)
print("\nFINAL RESULTS!!!")
print(results_df)
