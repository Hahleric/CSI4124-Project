from random import random


class Branch:
    def __init__(self, average_service_time):
        self.average_service_time = average_service_time

    def serve(self):
        return random.expovariate(1 / self.average_service_time)

