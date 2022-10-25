import numpy as np
from inverse_transform_sampling import generateExponential, generateBinomial
import scipy


class Simulation:

    def __init__(self):

        # Hyperparameter
        self.ARRIVAL_LAMBDA = 5
        self.NUMBER_OF_SEATS_ON_BUS = 5
        self.NUMBER_OF_BUS_STOPS = 10
        self.BAlKING_LENGTH_LOC = 10

        # Counter for the simulation
        self.clock = 0
        # Total number of arrival till the end of the simulation
        self.totalNumberOfArrivals = 0
        # Time of next arrival of customer
        self.timeOfNextArrival = generateExponential(lmbda = self.ARRIVAL_LAMBDA)
        # Departure time from server (bus) i
        self.departureTimes = [float('inf') for i in range(self.NUMBER_OF_SEATS_ON_BUS)]
        # Sum of serving times for each server in the simulation
        self.sumOfServingTimes = [0 for i in range(self.NUMBER_OF_SEATS_ON_BUS)]
        # Binary state of servers (bus) of whether serving or not presently
        self.presentStateOfServers = [0 for i in range(self.NUMBER_OF_SEATS_ON_BUS)]
        # Total wait time
        self.totalWaitingTime = 0
        # Total length of queue presently
        self.lengthOfQueue = 0
        # Total number of customers who had to wait in queue to be served
        self.cumulativeQueueLength = 0
        # Total number of customers in the queueing system
        self.lengthOfSystem = 0
        # Number of customers served by each server (bus)
        self.numberOfCustomersServed = [0 for i in range(self.NUMBER_OF_SEATS_ON_BUS)]
        # Number of customers who left without being served
        self.numberOfLostCustomers = 0

    def timing_routine(self):
        """
        The timing routine decides which event occurs next by comparing the scheduled time of events
        and advances the simulation clock to the respective event.
        Initially, the departure events are scheduled to occur at time infinity(since there are no customers),
        which guarantees that the first event will be an arrival event.
        :return:
        """

        timeToNextEvent = min(self.timeOfNextArrival, min(self.departureTimes))

        self.totalWaitingTime += (timeToNextEvent - self.clock) if self.lengthOfSystem > 0 else 0
        self.clock += timeToNextEvent

        if self.timeOfNextArrival < min(self.departureTimes):
            self.add_customer_to_queue()

        else:
            # FIND THE SERVER GETTING FREE THE FIRST
            for server, serving_time in enumerate(self.departureTimes):
                if self.departureTimes[server] < self.timeOfNextArrival and self.departureTimes[server] < all(
                        list(
                                map(
                                        lambda x: x > self.departureTimes[server],
                                        self.departureTimes[:server] + self.departureTimes[server + 1:]
                                        )
                                )
                        ):
                    self.serve_customer_in_queue(server = server)

    def _all_servers_are_busy(self):
        self.lengthOfQueue += 1
        self.cumulativeQueueLength += 1

    def _get_next_arrival(self):
        self.timeOfNextArrival = self.clock + generateExponential(self.ARRIVAL_LAMBDA)

    def _serve_customer(self, chosenServer: int):
        self.presentStateOfServers[chosenServer] = 1
        servingTime = generateBinomial(n = self.NUMBER_OF_BUS_STOPS)
        self.sumOfServingTimes[chosenServer] += self.departureTimes[chosenServer]
        self.departureTimes[chosenServer] = self.clock + servingTime

    def add_customer_to_queue(self):

        self.totalNumberOfArrivals += 1
        self.lengthOfSystem += 1

        if self.lengthOfQueue == 0:

            if all(list(map(lambda x: x == 1, self.presentStateOfServers))):

                self._all_servers_are_busy()
                self._get_next_arrival()

            elif all(list(map(lambda x: x == 0, self.presentStateOfServers))):

                chosenServer = np.random.choice(range(self.NUMBER_OF_SEATS_ON_BUS))
                self._serve_customer(chosenServer)
                self._get_next_arrival()

            else:
                chosenServer = self.presentStateOfServers.index(0)
                self._serve_customer(chosenServer)
                self._get_next_arrival()

        else:

            probabilityOfBalking = scipy.stats.expon.pdf(self.lengthOfQueue, loc = self.BAlKING_LENGTH_LOC)

            if np.random.uniform() < probabilityOfBalking:
                self.numberOfLostCustomers += 1

            else:
                self._all_servers_are_busy()
                self._get_next_arrival()

    def serve_customer_in_queue(self, server):

        self.numberOfCustomersServed[server] += 1
        self.lengthOfSystem -= 1

        if self.lengthOfQueue > 0:
            self._serve_customer(server)
            self.lengthOfQueue -= 1

        else:
            self.departureTimes[server] = float('inf')
            self.presentStateOfServers[server] = 0











