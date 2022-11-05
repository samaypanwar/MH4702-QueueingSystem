from collections import deque
from typing import List, Dict

"""File containing the required classes for our simulation"""

class Customer:
    def __init__(self, birth_time: float, system_customers: int, verbose: bool = False):
        """This class creates a new customer object that needs the lambda parameter for the birth process"""

        self.status = 'In Queue'
        # Time of arrival of the customer in the system
        self.arrival_time = birth_time
        # Time of entering the bus for the customer in the system
        self.boarded_time = float('inf')
        # Time of being served for the customer in the system
        self.departure_time = float('inf')
        # Number of people in system at time of arrival
        self.system_customers = system_customers

        self.verbose = verbose

    def board_bus(self, boarding_time: float):
        """Function that updates the status of the customer and notes down the time the customer boards the bus"""

        if self.verbose:
            print("Customer boards bus.")

        self.boarded_time = boarding_time
        self.status = 'On bus'

    def alight_bus(self, departure_time: float):
        """Function that updates the status of the customer and notes down the time the customer leaves the bus"""

        if self.verbose:
            print("Customer alights bus.")

        self.departure_time = departure_time
        self.status = 'Served'

    def calculate_stats(self):
        """This function returns all the relevant statistics for the customer while they were in the system"""

        return {
                'arrival_time'  : self.arrival_time,
                'boarded_time'  : self.boarded_time,
                'departure_time': self.departure_time,
                'waiting_time'  : self.boarded_time - self.arrival_time,
                'serving_time'  : self.departure_time - self.boarded_time,
                'time_in_system': self.departure_time - self.arrival_time,
                'customers_upon_arrival': self.system_customers,
                }


class BusStop:
    def __init__(self):
        """This class takes care of keeping track of the queue in our system"""

        # Number of customers in the queue presently
        self.customers = 0
        # Create an instance of a queue
        self.queue = deque()

    def customer_arrives(self, customer: Customer):
        """This function adds the newly arrived customer to the queue"""

        self.queue.append(customer)
        # Updated the number of customers in the queue
        self.customers += 1

    def customer_balks(self, customer: Customer):
        """This function removes the customer from the queue if they balk"""

        self.queue.remove(customer)
        # Updated the number of customers in the queue
        self.customers -= 1

    def serve_customer(self):
        """This function removes the customer from the queue if they are being served"""

        # If there is presently a queue
        if self.queue:
            # Remove a customer from the queue
            self.customers -= 1

            # Return the first customer in the queue (FIFO)
            return self.queue.popleft()


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


class Simulation:

    def __init__(
        self, bus_seats: int, bus_stops: int, 
        interarrival_times: List[float], serving_times: List[float],
        verbose: bool = False):
        """This class is responsible for managing the simulation of our system and keeping track of states and events"""

        # Hyper-parameters
        # Number of seats on a bus (servers)
        self.BUS_SEATS = bus_seats
        # Number of bus stops
        self.BUS_STOPS = bus_stops

        # Simulation Variables
        self.interarrival_times = interarrival_times
        self.serving_times = serving_times

        # System time
        self.time = 0

        # Instance of a queue of customers
        self.busStop = BusStop()
        # Instance of a set of servers
        self.bus = Bus(seats = self.BUS_SEATS, verbose = verbose)

        # Keep track of system statistics
        self.total_arrivals = 0
        self.total_boarded = 0
        self.total_served = 0
        self.system_customers = 0
        self.verbose = verbose
        self.customer_history = []

        # Get the next Events in the system
        self.time_to_next_arrival = self.generate_next_arrival()
        self.time_to_next_departure = float('inf')

    def calculate_statistics(self):
        """This function returns the relevant statistics to the simulation"""

        return {
                'arrivals': self.total_arrivals,
                'queue'   : self.busStop.customers,
                'served'  : self.total_served,
                'idle servers': self.bus.free_seats
                }

    def get_customer_history(self):
        """This function returns the customer history of all the customers served by the bus"""

        return self.bus.customer_history + [customer.calculate_stats() for customer in self.bus.seats if customer is
                                            not None] + [customer.calculate_stats() for customer in self.busStop.queue]

    def generate_next_arrival(self):
        """This function generates the next arrival time for a customer"""
        return self.time + self.interarrival_times[self.total_arrivals] if self.total_arrivals < (len(self.interarrival_times)-1) else float('inf')

    def generate_serving_time(self):
        """This function generates the next departure time for a customer"""
        return self.time + self.serving_times[self.total_boarded] if self.total_boarded < len(self.serving_times) else float('inf') 

    def time_step(self):
        """This function moves the simulation forward to the next step"""

        # Either a new customer arrives or an existing customer leaves after being served
        time_to_next_event = min(self.time_to_next_arrival, self.time_to_next_departure)

        # Update the system clock
        self.time = time_to_next_event

        if self.time_to_next_arrival < self.time_to_next_departure:

            if self.verbose:
                print("New customer arrives!")

            # A customer arrives at the bus stop
            self.customer_arrives()
        else:

            if self.verbose:
                print("Another customer served :)")

            # A customer leaves the bus after being served
            try:
                self.customers_alight()
            except:
                print(self.bus.seats)
                print(self.busStop.customers)
                print(self.total_arrivals)
                print(self.total_served)

    def customer_arrives(self):
        """This function takes care of when a customer is added to the queue after arriving"""

        # Create a new customer instance at the current time
        customer = Customer(self.time, self.system_customers, self.verbose)
        # Find the time that it will take to serve the newly arrived customer
        serving_time = self.generate_serving_time()

        # If there are free seats on the bus
        if self.bus.free_seats > 0:

            # Add the customer to the bus
            self.bus.customer_boards(customer, self.time, serving_time)
            self.total_boarded += 1
            # Update the next time that a customer is going to be served
            self.time_to_next_departure = self.bus.get_next_departure_time()

        else:

            # Add the customer to the queue
            self.busStop.customer_arrives(customer)

        # Find the next time that a customer is going to be arriving in the system
        self.time_to_next_arrival = self.generate_next_arrival()

        # Update system statistics
        self.total_arrivals += 1
        self.system_customers += 1

    def customers_alight(self):
        """This function takes care of when a customer leaves the bus after being served"""

        # Returns the number of customers served at the current time
        served = self.bus.customers_alight(self.time)
        # Update system statistics
        self.total_served += served
        self.system_customers -= served

        # While there are available seats on the bus and there is a queue
        while self.bus.free_seats > 0 and self.busStop.queue:

            # Get customers into the bus and find their serving times (FIFO)
            customer = self.busStop.serve_customer()
            serving_time = self.generate_serving_time()
            self.bus.customer_boards(customer, self.time, serving_time)
            self.total_boarded += 1

        # Update the next time that a customer is going to be served
        self.time_to_next_departure = self.bus.get_next_departure_time()
