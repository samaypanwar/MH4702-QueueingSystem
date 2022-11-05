from utils import Simulation
from typing import List, Dict
import pandas as pd
from inverse_transform_sampling import *

def run_simulation(
        bus_seats: int, bus_stops: int, 
        interarrival_times: List[float], serving_times: List[float],
        serving_limit: int = 100, verbose: bool = False):
    """This function goes through one simulation cycle of our system"""

    # Create a simulation object
    simulation = Simulation(bus_seats, bus_stops, interarrival_times, serving_times, verbose)

    # While the number of customers served is fewer than the serving limit for the simulation
    while simulation.total_served < serving_limit:

        if verbose:
            print(f"Current time is {simulation.time}.")

        # Time a time step till the next event in the simulation
        simulation.time_step()
        # Find the relevant statistics at that time step
        stats = simulation.calculate_statistics()

        if verbose:
            print(
                    f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}."
                  )
    if verbose:
        print("\nSimulation complete.")
        print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")

    return simulation.get_customer_history()


def aggregate_results(result: List[Dict]):
    """This function aggregates the results from each customer to the entire simulation"""

    temp = result[0].copy()

    for key in temp:
        temp[key] = []

    for customer in result:

        for key in customer.keys():
            temp[key].append(customer[key])

    result_df = pd.DataFrame(data = temp)

    return result_df


def run_experiment(
    iterations: int, arrival_lambda: float, bus_seats: int, bus_stops: int, variance_reduction: str = 'Standard MC',
    serving_limit: int = 100, verbose: bool = False):

    experiment_results = []

    for _ in range(iterations):

        # arrival_lambda = average number of customers in a time period
        if variance_reduction == 'Antithetic Variables':
            interarrival_times_list = [generate_exponential_antithetic(arrival_lambda) for _ in range(serving_limit)]
            serving_times_list = [[x+1 for x in generate_binomial_antithetic(n=bus_stops)] for _ in range(serving_limit)]

            for interarrival_times, serving_times in zip(zip(*interarrival_times_list), zip(*serving_times_list)):
                customer_history = run_simulation(bus_seats, bus_stops, interarrival_times, serving_times, serving_limit, verbose)
                customer_history = aggregate_results(customer_history)
                experiment_results.append({
                    'arrival_lambda': arrival_lambda,
                    'bus_seats': bus_seats,
                    'bus_stops': bus_stops,
                    'average_waiting_time': np.mean(customer_history['waiting_time']),
                    'average_time_in_system': np.mean(customer_history['time_in_system']),
                    'average_customers_upon_arrival': np.mean(customer_history['customers_upon_arrival'])
                })

        else: # Standard MC
            interarrival_times = [generate_exponential(arrival_lambda) for _ in range(serving_limit)]
            serving_times = [generate_binomial(n=bus_stops)+1 for _ in range(serving_limit)]

            customer_history = run_simulation(bus_seats, bus_stops, interarrival_times, serving_times, serving_limit, verbose)
            customer_history = aggregate_results(customer_history)
            experiment_results.append({
                'arrival_lambda': arrival_lambda,
                'bus_seats': bus_seats,
                'bus_stops': bus_stops,
                'average_waiting_time': np.mean(customer_history['waiting_time']),
                'average_time_in_system': np.mean(customer_history['time_in_system']),
                'average_customers_upon_arrival': np.mean(customer_history['customers_upon_arrival'])
            })

    results = pd.DataFrame(experiment_results)

    return {
        'arrival_lambda': arrival_lambda,
        'bus_seats': bus_seats,
        'bus_stops': bus_stops,
        'waiting_time_mean': np.mean(results['average_waiting_time']),
        'waiting_time_std': np.std(results['average_waiting_time']),
        'time_in_system_mean': np.mean(results['average_time_in_system']),
        'time_in_system_std': np.std(results['average_time_in_system']),
        'customers_upon_arrival_mean': np.mean(results['average_customers_upon_arrival']),
        'customers_upon_arrival_std': np.std(results['average_customers_upon_arrival']),
    }

