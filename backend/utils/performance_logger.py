import time


class LatencyTracker:

    def __init__(self):
        self.start_time = time.time()

    def stop(self):
        latency = (time.time() - self.start_time) * 1000
        return round(latency, 2)