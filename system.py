from branch import *
from customer import *
from queue import *
from quickpass import *
import random
class System:
    # QuickPass Parameters that will be tuned
    quick_path_flag = False
    quick_path_threshold = -1
    quick_path_percentage = -1

    # queueing parameters
    average_intra_arrival_time = -1
    average_service_time = -1
    number_of_desks = -1

    system_time = -1;
    time_lag = -1

    def __init__(self, average_intra_arrival_time, average_service_time, number_of_desks, time_lag):
        self.average_intra_arrival_time = average_intra_arrival_time
        self.average_service_time = average_service_time
        self.number_of_desks = number_of_desks
        self.time_lag = time_lag
        self.branches = []
        self.queue = RegularQueue(time_lag)
        self.quickpass = QuickPass()
        self.system_time = 0
        for i in range(number_of_desks - 1):
            self.branches.append(Branch(average_service_time))

    def run_simulation(self):
        while True:
            # generate new customer
                self.system_time += random.expovariate(1 / self.average_intra_arrival_time)
            customer = Customer(self.system_time)
            # generate return time

    def get_return_interval(self):
        self.queue.calculate_qp_return_time(self.system_time, self.average_service_time, self.number_of_desks)











