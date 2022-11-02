import pandas as pd
from simulation import run_simulation, aggregate_results

if __name__ == '__main__':
    verbose = False
    time_limit = 100
    results = []
    for arrival_lambda in [5, 6, 7, 8, 20]:
        for bus_seats in [10]:
            for bus_stops in [5]:
                results.append(
                        run_simulation(
                                arrival_lambda = arrival_lambda,
                                bus_seats = bus_seats,
                                bus_stops = bus_stops,
                                time_limit = time_limit,
                                verbose = verbose
                                )
                        )

    simulation_history = []
    for result in results:
        simulation_history.append(aggregate_results(result))

# TODO: Add logging statements
# TODO: Create more than one bus class update
