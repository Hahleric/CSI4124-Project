import random
import simpy
import matplotlib.pyplot as plt

# Parameters
NUM_SERVERS = 3
SERVICE_RATE = 1.0  # Mean service rate
ARRIVAL_RATE = 2.0  # Mean arrival rate
QUICK_PASS_THRESHOLD = 5  # Threshold to activate QuickPass
QUICK_PASS_PERCENTAGE = 0.2  # Percentage of customers for QuickPass
SIMULATION_TIME = 300  # Simulation time in minutes
FIXED_TIME_LAG = 10  # Fixed time lag for return time calculation

# Data collectors
waiting_times = []
queue_lengths = []
times = []


def calculate_return_time(t, n, mu, c, t0):
    time_adjustment = n / (mu * c)
    return_time_lower_bound = t + t0 + time_adjustment - 30
    return_time_upper_bound = t + t0 + time_adjustment + 30
    return_time_lower_bound = max(return_time_lower_bound, t)
    # Return a random time within the calculated interval
    return random.uniform(return_time_lower_bound, return_time_upper_bound)


def regular_customer(env, customer_id, counter, service_time, regular_queue):
    """Process for regular customers."""
    arrival_time = env.now
    with counter.request(priority=1) as req:
        yield req
        wait = env.now - arrival_time
        waiting_times.append(wait)  # Collect waiting time
        yield env.timeout(service_time)
        # Customer is done, remove from the queue
        regular_queue.remove(customer_id)
    # Update queue length after service
    times.append(env.now)
    queue_lengths.append(len(regular_queue))


def quick_pass_customer(env, customer_id, counter, service_time, return_time, regular_queue):
    """Process for QuickPass customers."""
    # Customer leaves the queue for QuickPass and will come back later
    regular_queue.remove(customer_id)
    yield env.timeout(return_time - env.now)  # Wait until the return time
    with counter.request(priority=0) as req:
        yield req
        yield env.timeout(service_time)
    # Update queue length after service
    times.append(env.now)
    queue_lengths.append(len(regular_queue))


def setup(env, num_servers, arrival_rate):
    """Sets up the bank simulation environment."""
    counter = simpy.PriorityResource(env, num_servers)
    regular_queue = []

    def arrival_process(env):
        """Process for customer arrivals."""
        customer_id = 0
        while True:
            is_quick_pass = (len(regular_queue) >= QUICK_PASS_THRESHOLD and
                             random.random() < QUICK_PASS_PERCENTAGE)
            service_time = random.expovariate(SERVICE_RATE)

            if is_quick_pass:
                return_time = calculate_return_time(env.now, len(regular_queue), SERVICE_RATE, NUM_SERVERS,
                                                    FIXED_TIME_LAG)
                # Customer goes for QuickPass, remove from regular queue temporarily
                regular_queue.append(customer_id)  # Add to queue, will be removed in quick_pass_customer
                env.process(quick_pass_customer(env, customer_id, counter, service_time, return_time, regular_queue))
            else:
                regular_queue.append(customer_id)
                env.process(regular_customer(env, customer_id, counter, service_time, regular_queue))

            # Update queue length upon arrival
            times.append(env.now)
            queue_lengths.append(len(regular_queue))

            customer_id += 1
            yield env.timeout(random.expovariate(arrival_rate))

    yield from arrival_process(env)


# Create and run the simulation environment
env = simpy.Environment()
env.process(setup(env, NUM_SERVERS, ARRIVAL_RATE))
env.run(until=SIMULATION_TIME)

# Visualization
plt.figure(figsize=(14, 5))

# Plotting queue length over time
plt.subplot(1, 2, 1)
plt.step(times, queue_lengths, where='post', label='Queue Length')
plt.xlabel('Time')
plt.ylabel('Queue Length')
plt.title('Queue Length Over Time')
plt.legend()

# Plotting waiting time
plt.subplot(1, 2, 2)
plt.hist(waiting_times, bins=30, alpha=0.7, label='Waiting Time')
plt.xlabel('Waiting Time')
plt.ylabel('Frequency')
plt.title('Waiting Time Distribution')
plt.legend()

plt.tight_layout()
plt.show()
