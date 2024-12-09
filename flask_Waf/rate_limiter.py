import time

class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.requests = {}

    def is_rate_limited(self, ip):
        current_time = time.time()
        if ip in self.requests:
            request_times = self.requests[ip]
            request_times = [t for t in request_times if current_time - t <= self.window]
            if len(request_times) >= self.limit:
                return True
            self.requests[ip] = request_times + [current_time]
        else:
            self.requests[ip] = [current_time]
        return False

