import numpy as np
import heapq

# Define a Customer class to represent each customer in the queue
class Customer:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_service_time = 0
        self.return_time = 0
        self.waiting_time = 0
        self.departure_time = 0

    def set_service_start(self, start_time):
        self.start_service_time = start_time
        self.waiting_time = start_time - self.arrival_time
        self.departure_time = start_time + self.service_time


# Define a Server class to represent each server
class Server:
    def __init__(self):
        self.end_time = 0  # Time when this server will be free

    def is_free(self, current_time):
        return self.end_time <= current_time

    def serve(self, customer):
        if self.is_free(customer.arrival_time):
            customer.set_service_start(customer.arrival_time)
        else:
            customer.set_service_start(self.end_time)
        self.end_time = customer.departure_time


def multi_server_queue(number_customer, number_servers, inter_arrival_time_mean, inter_arrival_time_deviation,
                       service_time_mean, service_time_deviation):
    # Initialize servers
    servers = [Server() for _ in range(number_servers)]

    # Priority queue for finding the next available server
    server_queue = [(0, i) for i in range(number_servers)]
    heapq.heapify(server_queue)

    # List to store customer objects
    customer_arr = []
    timer = 0

    # Generate all customers with arrival times and service times
    for i in range(number_customer):
        # If first customer, they arrive at time 0, otherwise generate inter-arrival time
        if i == 0:
            arrival_time = 0
        else:
            arrival_time = np.abs(np.random.normal(inter_arrival_time_mean, inter_arrival_time_deviation)) + \
                           customer_arr[-1].arrival_time

        # Generate service time for the customer
        service_time = np.abs(np.random.normal(service_time_mean, service_time_deviation))

        customer_arr.append(Customer(arrival_time, service_time))

    # Simulate the queue
    for customer in customer_arr:
        # Get the next available server
        _, server_index = heapq.heappop(server_queue)
        server = servers[server_index]

        # Serve the customer
        server.serve(customer)

        # Update the server's availability in the priority queue
        heapq.heappush(server_queue, (server.end_time, server_index))

    return customer_arr


# Function to initiate the simulation
def simulation_start():
    number_customer = int(input("Enter number of customers: "))
    number_servers = int(input("Enter number of servers: "))
    inter_arrival_time_mean = float(input("Enter inter arrival time mean value in seconds: "))
    inter_arrival_time_deviation = float(input("Enter inter arrival time standard deviation value in seconds: "))
    service_time_mean = float(input("Enter service time mean in seconds: "))
    service_time_deviation = float(input("Enter service time standard deviation in seconds: "))

    customer_arr = multi_server_queue(number_customer, number_servers, inter_arrival_time_mean,
                                      inter_arrival_time_deviation,
                                      service_time_mean, service_time_deviation)

    # Print results for each customer
    for i, customer in enumerate(customer_arr, start=1):
        print(
            f"Customer {i}: Waiting Time = {customer.waiting_time:.2f} sec, Total System Time = {customer.departure_time - customer.arrival_time:.2f} sec")


simulation_start()
