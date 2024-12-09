from collections import defaultdict
import time

class AnomalyDetection:
    def __init__(self, threshold=10):
        self.threshold = threshold
        self.request_count = defaultdict(int)
        self.last_reset = time.time()
        self.reset_interval = 60  # Reset counters every 60 seconds

    def is_anomalous(self, request):
        current_time = time.time()
        if current_time - self.last_reset > self.reset_interval:
            self.request_count.clear()
            self.last_reset = current_time

        ip = request.remote_addr
        self.request_count[ip] += 1

        if self.request_count[ip] > self.threshold:
            return True

        # Check for unusual patterns in headers
        if self._check_unusual_headers(request.headers):
            return True

        # Check for unusual payload size
        content_length = request.headers.get('Content-Length', 0)
        if int(content_length) > 1000000:  # 1MB
            return True

        return False

    def _check_unusual_headers(self, headers):
        unusual_headers = ['X-Forwarded-For', 'X-Real-IP', 'X-Originating-IP']
        return any(header in headers for header in unusual_headers)

