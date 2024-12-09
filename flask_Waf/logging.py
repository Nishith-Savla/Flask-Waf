import logging
from flask import request
import json
from datetime import datetime

class WAFLogger:
    def __init__(self, log_file='waf.log'):
        self.logger = logging.getLogger('flask_waf')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_request(self, req):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': req.method,
            'url': req.url,
            'headers': dict(req.headers),
            'body': req.get_data(as_text=True),
            'remote_addr': req.remote_addr
        }
        self.logger.info(f"Request: {json.dumps(log_data)}")

    def log_violations(self, req, violations):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': req.method,
            'url': req.url,
            'remote_addr': req.remote_addr,
            'violations': violations
        }
        self.logger.warning(f"Violations: {json.dumps(log_data)}")

    def log_blocked_request(self, req, reason):
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': req.method,
            'url': req.url,
            'remote_addr': req.remote_addr,
            'reason': reason
        }
        self.logger.warning(f"Blocked Request: {json.dumps(log_data)}")

    def log_error(self, message):
        self.logger.error(message)

