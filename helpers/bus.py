from typing import List, Dict
from helpers.customer import Customer

"""File containing the required classes for our simulation"""

class Bus:
    def __init__(self, seats: int, customer_history: List[Dict] = None, verbose: bool = False):

        """This class is responsible for acting as the servers in our system"""

        # Instantiate empty seats in the bus
        self.seats = [None for _ in range(seats)]
        # Get the departure time for each seat in the bus
        self.departure_times = [float('inf')] * seats
        # Note the number of free seats in the bus
        self.free_seats = seats
        # Note the number of customers served by the bus
        self.total_customers_served = 0

        self.verbose = verbose

        if customer_history is None:
            customer_history = list()

        self.customer_history = customer_history

    def get_next_departure_time(self):
        """This function gets the minimum next time that a customer leaves his seat (has been served)"""
        return min(self.departure_times)

    def customer_boards(self, customer: Customer, time: float, serving_time: float):
        """This function finds the entering customer a seat in the bus (begins being served)"""
        if self.free_seats == 0:

            if self.verbose:
                print("No seats available!")

            return

        # Find the first available seat in the bus
        available_seat = self.seats.index(None)
        # Assign that seat to the new customer
        self.seats[available_seat] = customer
        # Update the boarding time of the new customer
        customer.board_bus(time)
        # Set the departure time of the customer as the time the customer would be leaving
        self.departure_times[available_seat] = serving_time
        # Update the number of free seats in the bus
        self.free_seats -= 1

    def customers_alight(self, current_time: float):
        """This function takes into account the code flow when a customer is done being served"""

        customers_served = 0

        # Possible that multiple customers may have identical serving times
        while current_time in self.departure_times and customers_served <= len(self.seats):
            # Get the serving time for the customer who is supposed to leave at the current time
            seat_number = self.departure_times.index(current_time)
            # Get the customer who is supposed to leave at the current time
            customer = self.seats[seat_number]
            # Make them leave
            customer.alight_bus(current_time)
            self.customer_history.append(customer.calculate_stats())

            if self.verbose:
                print(customer.calculate_stats())

            # Update the seat and departure time of the empty seat number
            self.seats[seat_number] = None
            self.departure_times[seat_number] = float('inf')
            # Update the relevant statistics
            self.free_seats += 1
            self.total_customers_served += 1
            customers_served += 1

        # Return the number of customers served in the current timestep
        return customers_served

    def calculate_stats(self):
        """This function returns the relevant statistics for our class of servers"""

        return {'total_customers_served': self.total_customers_served}