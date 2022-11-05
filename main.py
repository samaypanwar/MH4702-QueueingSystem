import pandas as pd
from simulation import run_experiment
from tqdm import tqdm

if __name__ == '__main__':

    verbose = False
    time_limit = float("inf") # no time limit
    serving_limit = 1000
    iterations = 10
    standard_mc_results = []
    antithetic_variables_results = []

    for arrival_lambda in [20, 50]:
        for bus_seats in [10, 50, 100]:
            for bus_stops in tqdm([5, 10, 20]):

                antithetic_variables_results.append(run_experiment(
                    iterations=iterations // 2,
                    arrival_lambda=arrival_lambda,
                    bus_seats=bus_seats,
                    bus_stops=bus_stops,
                    variance_reduction='Antithetic Variables',
                    serving_limit=serving_limit,
                    verbose=verbose))

                print(antithetic_variables_results[-1])

                standard_mc_results.append(run_experiment(
                    iterations=iterations,
                    arrival_lambda=arrival_lambda,
                    bus_seats=bus_seats,
                    bus_stops=bus_stops,
                    variance_reduction='Standard MC',
                    serving_limit=serving_limit,
                    verbose=verbose))

                print(standard_mc_results[-1])

    antithetic_variables_df = pd.DataFrame(antithetic_variables_results)
    standard_mc_df = pd.DataFrame(standard_mc_results)

    print("Standard MC results:")
    print(standard_mc_df)
    print("\nAntithetic Variables results:")
    print(antithetic_variables_df)

    antithetic_variables_df.to_csv('antithetic_variables_results.csv')
    standard_mc_df.to_csv('standard_mc_results.csv')
                

# TODO: Add logging statements
# TODO: Create more than one bus class update
