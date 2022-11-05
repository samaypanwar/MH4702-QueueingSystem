from collections import deque
from helpers.customer import Customer

"""File containing BusStop class for our simulation"""

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