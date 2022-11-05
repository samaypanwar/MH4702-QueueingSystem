"""File containing Customer class for our simulation"""

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
