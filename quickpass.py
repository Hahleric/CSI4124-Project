class QuickPass:
    def __init__(self):
        self.queue = []

    def enqueue(self, customer):
        self.queue.append(customer)

    def dequeue(self):
        return self.queue.pop(0)

    # enqueue with customer list
    def enqueue_list(self, customer_list):
        self.queue.extend(customer_list)

    def is_empty(self):
        return len(self.queue) == 0
    