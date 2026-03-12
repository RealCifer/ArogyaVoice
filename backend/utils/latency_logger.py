import time

def measure_latency(start_time):
    """
    Calculates latency in milliseconds.
    """
    latency = (time.time() - start_time) * 1000
    return round(latency, 2)