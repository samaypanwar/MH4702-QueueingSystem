from inverse_transform_sampling import generate_exponential, generate_binomial
from collections import deque

class Customer:
    def __init__(self, birth_time: float):
        self.status = 'In queue'
        self.arrival_time = birth_time
        self.boarded_time = float('inf')
        self.departure_time = float('inf')

    def board_bus(self, time: float):
        print("Customer boards bus.")
        self.boarded_time = time
        self.status = 'On bus'

    def alight_bus(self, departure_time: float):
        print("Customer alights bus.")
        self.departure_time = departure_time
        self.status = 'Served'

    def calculate_stats(self):
        return {
            'arrival_time': self.arrival_time,
            'boarded_time': self.boarded_time,
            'departure_time': self.departure_time,
            'waiting_time': self.boarded_time - self.arrival_time,
            'serving_time': self.departure_time - self.boarded_time,
            'time_in_system': self.departure_time - self.arrival_time
        }

class BusStop:
    def __init__(self):
        self.customers = 0
        self.queue = deque()

    def customer_arrives(self, customer: Customer):
        self.queue.append(customer)
        self.customers += 1
    
    def customer_leaves(self, customer: Customer):
        self.queue.remove(customer)
        self.customers -= 1

    def serve_customer(self):
        if self.queue:
            self.customers -= 1
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
        self.ARRIVAL_LAMBDA = arrival_lambda # number of customers in a time period
        self.BUS_SEATS = bus_seats # number of seats on a bus (servers)
        self.BUS_STOPS = bus_stops # number of bus stops

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
            'queue': self.busstop.customers,
            'served': self.total_served
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
            self.customer_arrives() # bus stop
        else:
            print("Another customer served (:")
            self.customers_alight() # bus

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