import pandas as pd
from simulation import get_average_queue_length, run_simulation, aggregate_results, get_average_waiting_time, \
    get_average_serving_time

if __name__ == '__main__':

    if __name__ == '__main__':
        verbose = False
        time_limit = 1000
        results = []
        sim_stats = []
        for arrival_lambda in [5]:
            for bus_seats in [10]:
                for bus_stops in [5]:
                    customer_results, system_results = run_simulation(
                            arrival_lambda = arrival_lambda,
                            bus_seats = bus_seats,
                            bus_stops = bus_stops,
                            time_limit = time_limit,
                            verbose = verbose
                            )
                    results.append(
                            [customer_results, system_results]
                            )

        simulation_history = []
        for result in results:
            simulation_history.append([aggregate_results(result[0]), aggregate_results(result[1])])
            sim_stats.append([get_average_waiting_time(simulation_history[-1]), get_average_serving_time(
                    simulation_history[-1]), get_average_queue_length(simulation_history[-1])])


            print(f"Simulation Statistics: W = {sim_stats[-1][0]}, L = {sim_stats[-1][2]}, Average Serving Time = "
                  f"{sim_stats[-1][1]}")

# TODO: Add logging statements

