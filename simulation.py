from helpers.simulation import Simulation
from typing import List, Dict
import pandas as pd
from utils.inverse_transform_sampling import *
import numpy as np
from tqdm import tqdm

# overlap between this and run_experiment
def get_statistics_distribution(arrival_lambda: float, bus_seats: int, bus_stops: int, time_limit: float = 100,
                                verbose: bool = False, runs: int = 1000, counter = True):
    stats = {'W': [], 'L': [], 'S': []}

    if counter:

        for _ in tqdm(range(runs)):

            result = run_simulation(
                            arrival_lambda = arrival_lambda,
                            bus_seats = bus_seats,
                            bus_stops = bus_stops,
                            time_limit = time_limit,
                            verbose = verbose
                            )

            stats['W'].append(result['average_waiting_time'])
            stats['L'].append(result['average_queue_length'])
            stats['S'].append(result['average_serving_time'])
    else:

        for _ in range(runs):
            result = run_simulation(
                    arrival_lambda = arrival_lambda,
                    bus_seats = bus_seats,
                    bus_stops = bus_stops,
                    time_limit = time_limit,
                    verbose = verbose
                    )

            stats['W'].append(result['average_waiting_time'])
            stats['L'].append(result['average_queue_length'])
            stats['S'].append(result['average_serving_time'])

    return pd.DataFrame(data = stats)

def run_simulation(
        bus_seats: int, bus_stops: int, 
        interarrival_times: List[float], serving_times: List[float],
        serving_limit: int = 100, time_limit: float = float('inf'), verbose: bool = False):

    """This function goes through one simulation cycle of our system"""

    # Create a simulation object
    simulation = Simulation(bus_seats, bus_stops, interarrival_times, serving_times, verbose)

    # While the number of customers served is fewer than the serving limit for the simulation
    # and system clock is less than our limit (2 ways of controlling simulation length)
    step_results = []
    
    while simulation.total_served < serving_limit and simulation.time < time_limit:

        if verbose:
            print(f"Current time is {simulation.time}.")

        # Time a time step till the next event in the simulation
        simulation.time_step()
        # Find the relevant statistics at that time step
        stats = simulation.calculate_statistics()
        step_results.append(stats)

        if verbose:
            print(f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}.")

    if verbose:
        print("\nSimulation complete.")
        print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")

    customer_results, system_results = aggregate_results(simulation.get_customer_history()), aggregate_results(step_results)
    
    return {
        'average_waiting_time': get_average_waiting_time(customer_results),
        'average_queue_length': get_average_queue_length(system_results),
        'average_serving_time': get_average_serving_time(customer_results),
        'average_customers_upon_arrival': np.mean(customer_results['customers_upon_arrival'])}


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
    serving_limit: int = 100, time_limit: float = float('inf'), verbose: bool = False):

    experiment_results = []

    for _ in range(iterations):

        # arrival_lambda = average number of customers in a time period
        if variance_reduction == 'Antithetic Variables':
            interarrival_times = [generate_exponential_antithetic(arrival_lambda) for _ in range(serving_limit)]
            serving_times = [generate_binomial_antithetic(n=bus_stops)+1 for _ in range(serving_limit)]
            iterations = iterations // 2

        elif variance_reduction == 'Stratified Sampling':
            interarrival_times = generate_exponential_stratified(arrival_lambda, serving_limit, 10)
            serving_times = [x+1 for x in generate_binomial_stratified(n=bus_stops, num_samples=serving_limit, bins=10)]

        else: # Standard MC
            interarrival_times = [generate_exponential(arrival_lambda) for _ in range(serving_limit)]
            serving_times = [generate_binomial(n=bus_stops)+1 for _ in range(serving_limit)]
        
        customer_history = run_simulation(bus_seats, bus_stops, interarrival_times, serving_times, serving_limit, time_limit, verbose)
        experiment_results.append({
            'arrival_lambda': arrival_lambda,
            'bus_seats': bus_seats,
            'bus_stops': bus_stops,
            'average_waiting_time': customer_history['average_waiting_time'],
            'average_serving_time': customer_history['average_serving_time'],
            'average_queue_length': customer_history['average_queue_length'],
            'average_customers_upon_arrival': customer_history['average_customers_upon_arrival'],
        })

    results = pd.DataFrame(experiment_results)

    return {
        'arrival_lambda': arrival_lambda,
        'bus_seats': bus_seats,
        'bus_stops': bus_stops,
        'waiting_time_mean': np.mean(results['average_waiting_time']),
        'waiting_time_std': np.std(results['average_waiting_time']),
        'serving_time_mean': np.mean(results['average_serving_time']),
        'serving_time_std': np.std(results['average_serving_time']),
        'customers_upon_arrival_mean': np.mean(results['average_customers_upon_arrival']),
        'customers_upon_arrival_std': np.std(results['average_customers_upon_arrival']),
    }


def get_average_waiting_time(customer_results: pd.DataFrame) -> float:
    """
    This function returns the average waiting time
    Parameters
    ----------
    result_df : dataframe that contain information about the simulation

    Returns
    -------
    The average waiting time before being served
    """

    return customer_results[customer_results.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().waiting_time


def get_average_serving_time(customer_results: pd.DataFrame) -> float:
    """
    This function returns the average serving time
    Parameters
    ----------
    customer_results : dataframe that contain information about the simulation

    Returns
    -------
    The average serving time in the bus before the customer alights
    """

    return customer_results[customer_results.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().serving_time


def get_average_queue_length(system_results: pd.DataFrame) -> float:
    """
    This function returns the average queue length
    Parameters
    ----------
    system_results : dataframe that contain information about the simulation

    Returns
    -------
    This function returns the average queue length
    """

    return system_results[system_results.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().queue

