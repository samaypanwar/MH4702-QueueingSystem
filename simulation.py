from inverse_transform_sampling import generate_exponential, generate_binomial
from collections import deque

"""File containing the required classes for our simulation"""


class Customer:
    def __init__(self, birth_time: float, verbose: bool = False):
        """This class creates a new customer object that needs the lambda parameter for the birth process"""

        self.status = 'In Queue'
        # Time of arrival of the customer in the system
        self.arrival_time = birth_time
        # Time of entering the bus for the customer in the system
        self.boarded_time = float('inf')
        # Time of being served for the customer in the system
        self.departure_time = float('inf')

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
                'time_in_system': self.departure_time - self.arrival_time
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
    def __init__(self, seats: int):
        self.seats = [None] * seats
        self.departure_times = [float('inf')] * seats
        self.free_seats = seats
        self.total_customers_served = 0

    def get_next_departure_time(self):
        return min(self.departure_times)

    def customer_boards(self, customer: Customer, time: float, serving_time: float):
        if self.free_seats == 0:
            print("No seats available!")
            return

        available_seat = self.seats.index(None)
        self.seats[available_seat] = customer
        customer.board_bus(time)
        self.departure_times[available_seat] = serving_time
        self.free_seats -= 1

    def customers_alight(self, current_time: float):
        served = 0
        while current_time in self.departure_times:
            seat = self.departure_times.index(current_time)
            customer = self.seats[seat]
            customer.alight_bus(current_time)
            print(customer.calculate_stats())
            self.seats[seat] = None
            self.departure_times[seat] = float('inf')
            self.free_seats += 1
            self.total_customers_served += 1
            served += 1
        return served

    def calculate_stats(self):
        return {'total_customers_served': self.total_customers_served}


class SimulationStuff:

    def __init__(self, arrival_lambda, bus_seats, bus_stops):
        # Hyperparameter
        self.ARRIVAL_LAMBDA = arrival_lambda  # number of customers in a time period
        self.BUS_SEATS = bus_seats  # number of seats on a bus (servers)
        self.BUS_STOPS = bus_stops  # number of bus stops

        self.time = 0
        self.busstop = BusStop()
        self.bus = Bus(self.BUS_SEATS)

        self.t_next_arrival = self.generate_next_arrival()
        self.t_next_departure = float('inf')

        self.total_arrivals = 0
        self.total_served = 0

    def calculate_stats(self):
        return {
                'arrivals': self.total_arrivals,
                'queue'   : self.busstop.customers,
                'served'  : self.total_served
                }

    def generate_next_arrival(self):
        return self.time + generate_exponential(self.ARRIVAL_LAMBDA)

    def generate_serving_time(self):
        return self.time + generate_binomial(n = self.BUS_STOPS)

    def time_step(self):
        t_next_event = min(self.t_next_arrival, self.t_next_departure)
        self.time = t_next_event

        if self.t_next_arrival < self.t_next_departure:
            print("New customer arrives!")
            self.customer_arrives()  # bus stop
        else:
            print("Another customer served (:")
            self.customers_alight()  # bus

    def customer_arrives(self):
        customer = Customer(self.time)
        serving_time = self.generate_serving_time()
        if self.bus.free_seats > 0:
            self.bus.customer_boards(customer, self.time, serving_time)
            self.t_next_departure = self.bus.get_next_departure_time()
        else:
            self.busstop.customer_arrives(customer)
        self.t_next_arrival = self.generate_next_arrival()
        self.total_arrivals += 1

    def customers_alight(self):
        served = self.bus.customers_alight(self.time)
        self.total_served += served
        while self.bus.free_seats > 0 and self.busstop.queue:
            customer = self.busstop.serve_customer()
            serving_time = self.generate_serving_time()
            self.bus.customer_boards(customer, self.time, serving_time)
        self.t_next_departure = self.bus.get_next_departure_time()
