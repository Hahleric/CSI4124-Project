import random

class Customer:
    def __init__(self, intra_arrival):
        self.intra_arrival = intra_arrival
        self.return_time = -1

    def set_return_time(self, return_interval, current_time):
        self.return_time = current_time + return_interval
