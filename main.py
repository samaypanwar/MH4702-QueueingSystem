import pandas as pd
from utils.simulation import run_experiment
from tqdm import tqdm

if __name__ == '__main__':

    verbose = False
    time_limit = float("inf") # no time limit
    serving_limit = 1000
    iterations = 10
    variance_reduction_techniques = ['Standard MC', 'Antithetic Variables', 'Stratified Sampling', 'Control Variates']
    all_results = {technique: [] for technique in variance_reduction_techniques}

    for arrival_lambda in [20, 50]:
        for bus_seats in [50, 100]:
            for bus_stops in tqdm([5, 10, 20]):

                for technique in variance_reduction_techniques:

                    result = run_experiment(
                        iterations=iterations,
                        arrival_lambda=arrival_lambda,
                        bus_seats=bus_seats,
                        bus_stops=bus_stops,
                        variance_reduction=technique,
                        serving_limit=serving_limit,
                        time_limit=time_limit,
                        verbose=verbose
                    )

                    print(f"{technique}: {result}")
                    all_results[technique].append(result)

    for technique in variance_reduction_techniques:
        all_results[technique] = pd.DataFrame(all_results[technique])
        print(f"{technique} results:\n{all_results[technique]}\n")
        all_results[technique].to_csv(f"data\{technique} Results-3.csv")

# TODO: Add logging statements
