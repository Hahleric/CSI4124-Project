class RegularQueue:
    def __init__(self, time_lag):
        self.queue = []
        self.time_lag = time_lag

    def __len__(self):
        return len(self.queue)

    def enqueue(self, customer):
        self.queue.append(customer)

    def dequeue(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def calculate_qp_return_time(self, system_time, average_service_time, desk_number):
        lower_bound = system_time + self.time_lag + len(self.queue) / desk_number * average_service_time - 30
        upper_bound = system_time + self.time_lag + len(self.queue) / desk_number * average_service_time + 30
        return [lower_bound, upper_bound]

    def pop_customers_by_percentage(self, percentage):
        if percentage > 1 or percentage < 0:
            raise ValueError("Percentage should be between 0 and 1")
        number_of_customers = int(len(self.queue) * percentage)
        customers = self.queue[:number_of_customers]
        self.queue = self.queue[number_of_customers:]
        return customers
