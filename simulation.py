from utils import Simulation
from typing import List, Dict
import pandas as pd


def run_simulation(
        arrival_lambda: float, bus_seats: int, bus_stops: int, time_limit: float = 100, verbose: bool = False
        ):
    """This function goes through one simulation cycle of our system"""

    # Create a simulation object
    simulation = Simulation(arrival_lambda, bus_seats, bus_stops, verbose)

    # While the system clock is less than our limit
    while simulation.time < time_limit:

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
