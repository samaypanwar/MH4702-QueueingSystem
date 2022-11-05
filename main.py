import pandas as pd
from simulation import get_average_queue_length, run_simulation, aggregate_results, get_average_waiting_time, \
    get_average_serving_time, get_statistics_distribution

if __name__ == '__main__':

    verbose = False

    time_limit = 720
    arrival_lambda = 1
    bus_seats = 50
    bus_stops = 10
    result = run_simulation(
                        arrival_lambda = arrival_lambda,
                        bus_seats = bus_seats,
                        bus_stops = bus_stops,
                        time_limit = time_limit,
                        verbose = verbose
                        )

    print(
            f"Simulation Statistics: W = {result[0]}, L = {result[1]}, Average Serving Time = "
            f"{result[2]}"
            )

# TODO: Add logging statements
