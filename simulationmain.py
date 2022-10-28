import numpy as np
from inverse_transform_sampling import generateExponential, generateBinomial
import scipy
from collections import deque

class Customer:
    def __init__(self):
        self.arrival_time = 0
        self.served_time = 0
        self.waiting_time = 0
        self.serving_time = 0
        self.time_in_system = self.departure_time - self.arrival_time

class BusStop:
    def __init__(self):
        self.customers = 0
        self.queue = deque()

    def customer_arrives(self, customer: Customer):
        self.queue.append(customer)
    
    def customer_leaves(self, customer: Customer):
        self.queue.remove(customer)

    def serve_customer(self):
        if not self.queue.empty():
            self.queue.pop(0)

class Bus:
    def __init__(self, seats):
        self.seats = [Seat() for _ in range(seats)]
        self.taken_seats = 0
        self.free_seats = seats
        self.total_customers_served = 0

    def customer_alights(self, customer: Customer):
        pass

class Seat:
    def __init__(self):
        self.taken = 0

    def customer_arrives(self):
        self.taken = 1

    def customer_leaves(self):
        self.taken = 0

class SimulationStuff:
    
    def __init__(self):
        self.time = 0
        self.busstop = BusStop()
        self.bus = Bus()

        self.t_next_arrival = self.generate_next_arrival()
        self.t_next_departure = float('inf')

        self.total_arrivals = 0
        self.total_served = 0

        # Hyperparameter
        self.ARRIVAL_LAMBDA = 5
        self.NUMBER_OF_SEATS_ON_BUS = 5
        self.NUMBER_OF_BUS_STOPS = 10
        self.BAlKING_LENGTH_LOC = 10
    
    def time_step(self):
        t_next_event = min(self.t_next_arrival, self.t_next_departure)
        self.time = t_next_event

        if self.t_next_arrival < self.t_next_departure:
            print("New customer arrives!")
            self.customer_arrives()
        else:
            print("Another customer served (:")
            self.customer_alights(self.bus)
    
    def generate_next_arrival(self):
        return self.time + generateExponential(self.ARRIVAL_LAMBDA)

    def generate_serving_time(self):
        return self.time + generateBinomial(n = self.NUMBER_OF_BUS_STOPS)

    def customer_arrives(self):
        customer = Customer()
        if self.bus.free_seats > 0:
            self.customer_boards(customer)
        else:
            self.customer_queues(customer)
        self.t_next_arrival = self.generate_next_arrival()
    
    def customer_queues(self, customer: Customer):
        pass

    def customer_boards(self, customer: Customer):
        pass

    def customer_alights(self, bus: Bus):
        bus.customer_alights()
        if not self.busstop.queue.empty():
            self.serve_customer(bus)
            self.generate_serving_time()

    def serve_customer(self, bus: Bus):
        customer = bus_stop

        # Show the server as busy
        self.presentStateOfServers[chosenServer] = 1
        # Generate the serving time for the customer being served as a binomial sum
        servingTime = generateBinomial(n = self.NUMBER_OF_BUS_STOPS)
        self.sumOfServingTimes[chosenServer] += self.departureTimes[chosenServer]
        # Update the last time a customer was served for each server
        self.departureTimes[chosenServer] = self.time + servingTime