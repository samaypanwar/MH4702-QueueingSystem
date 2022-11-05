from typing import List
from helpers.customer import Customer
from helpers.bus_stop import BusStop
from helpers.bus import Bus

"""File containing the Simulation object class for our simulation"""

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
