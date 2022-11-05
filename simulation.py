from utils import Simulation
from typing import List, Dict
import pandas as pd
import numpy as np
from tqdm import tqdm

def get_statistics_distribution(arrival_lambda: float, bus_seats: int, bus_stops: int, time_limit: float = 100,
                                verbose: bool = False, runs: int = 1000
                                ):
    stats = {'W': [], 'L': [], 'S': []}
    for i in tqdm(range(runs)):
        result = run_simulation(
                        arrival_lambda = arrival_lambda,
                        bus_seats = bus_seats,
                        bus_stops = bus_stops,
                        time_limit = time_limit,
                        verbose = verbose
                        )

        stats['W'].append(result[0])
        stats['L'].append(result[1])
        stats['S'].append(result[2])

    return pd.DataFrame(data = stats)
def run_simulation(
        arrival_lambda: float, bus_seats: int, bus_stops: int, time_limit: float = 100, verbose: bool = False
        ):
    """This function goes through one simulation cycle of our system"""

    # Create a simulation object
    simulation = Simulation(arrival_lambda, bus_seats, bus_stops, verbose)

    step_results = []

    # While the system clock is less than our limit
    while simulation.time < time_limit:

        if verbose:
            print(f"Current time is {simulation.time}.")

        # Time a time step till the next event in the simulation
        simulation.time_step()
        # Find the relevant statistics at that time step
        stats = simulation.calculate_statistics()
        step_results.append(stats)

        if verbose:
            print(
                    f"Total arrivals: {stats['arrivals']}, total queue length: {stats['queue']}, total served: {stats['served']}."
                  )
    if verbose:
        print("\nSimulation complete.")
        print(f"Total arrivals is {simulation.total_arrivals} with {simulation.total_served} actually served.")

    customer_results, system_results = aggregate_results(simulation.get_customer_history()), aggregate_results(
            step_results)

    W = get_average_waiting_time(customer_results)
    L = get_average_queue_length(system_results)
    S = get_average_serving_time(customer_results)

    return [W, L, S]


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

