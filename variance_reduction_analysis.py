import pandas as pd
from utils.simulation import run_experiment
from tqdm import tqdm
import time

verbose = False
time_limit = float("inf") # no time limit
serving_limit = 1000
iterations_list = [10, 100, 1000, 10000]
variance_reduction_techniques = ['Standard MC', 'Antithetic Variables', 'Stratified Sampling', 'Control Variates']
all_results = []

arrival_lambda = 3
bus_seats = 38 
bus_stops = 25

for iterations in iterations_list:

    for technique in variance_reduction_techniques:

        start = time.process_time()

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

        time_taken = time.process_time() - start

        print(f"{technique}: {result} took time {time_taken} to compute.")
        result['computation_time'] = time_taken
        result_df = pd.DataFrame([result])
        result_df.to_csv(f"data/variance/{technique}-result-{iterations}.csv")
        all_results.append(result)
        print()

all_results = pd.DataFrame(all_results)
print(all_results)

all_results.to_csv(f"data/variance/all-results.csv")