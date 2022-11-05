from utils import Simulation
from typing import List, Dict
import pandas as pd
import numpy as np


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

    return simulation.get_customer_history(), step_results


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

def get_average_waiting_time(result_df: List[pd.DataFrame]) -> float:
    """
    This function returns the average waiting time
    Parameters
    ----------
    result_df : list of our two dataframe that contain information about the simulation

    Returns
    -------
    The average waiting time before being served
    """

    return result_df[0][result_df[0].replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().waiting_time

def get_average_serving_time(result_df: List[pd.DataFrame]) -> float:
    """
    This function returns the average serving time
    Parameters
    ----------
    result_df : list of our two dataframe that contain information about the simulation

    Returns
    -------
    The average serving time in the bus before the customer alights
    """


    return result_df[0][result_df[0].replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().serving_time

def get_average_queue_length(result_df: List[pd.DataFrame]) -> float:
    """
    This function returns the average queue length
    Parameters
    ----------
    result_df : list of our two dataframe that contain information about the simulation

    Returns
    -------
    This function returns the average queue length
    """

    return result_df[1][result_df[1].replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)].mean().queue

