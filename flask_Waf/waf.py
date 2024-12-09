from flask import abort , request
from werkzeug.exceptions import HTTPException
from .rules import RuleEngine
from .logging import WAFLogger
from .config import WAFConfig
from .rate_limiter import RateLimiter
from .session_protection import SessionProtection
from .content_security import ContentSecurityPolicy
from .threat_intelligence import ThreatIntelligence
from .anomaly_detection import AnomalyDetection

class WAF:
    def __init__(self, app=None, config_file=None):
        self.app = app
        self.config = WAFConfig()
        if config_file:
            self.config.load_from_file(config_file)
        self.rule_engine = RuleEngine()
        self.logger = WAFLogger()
        self.rate_limiter = RateLimiter(self.config.rate_limit, 60)  # 60 seconds window
        self.session_protection = SessionProtection()
        self.csp = ContentSecurityPolicy()
        self.threat_intel = ThreatIntelligence()
        self.anomaly_detection = AnomalyDetection()
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.check_request)
        app.after_request(self.add_security_headers)

    def check_request(self):
        # Basic checks
        self._check_request_size()
        self._check_url_length()
        self._check_query_params()
        self._check_headers()
        self._check_rate_limit()
        # Advanced checks
        self._check_threat_intelligence()
        self._check_anomalies()

      
    def _check_request_size(self):
        if int(request.headers.get('Content-Length', 0)) > self.config.max_request_size:
            self.logger.log_blocked_request(request, "Payload too large")
            abort(413, description="Payload too large")
    def _check_url_length(self):
        if len(request.url) > self.config.max_url_length:
            self.logger.log_blocked_request(request, "URI too long")
            abort(414, description="URI too long")

    def _check_query_params(self):
        if len(request.args) > self.config.max_query_params:
            self.logger.log_blocked_request(request, "Too many query parameters")
            abort(400, description="Too many query parameters")

    def _check_headers(self):
        if len(request.headers) > self.config.max_headers:
            self.logger.log_blocked_request(request, "Too many headers")
            abort(400, description="Too many headers")

        for header in self.config.required_headers:
            if header not in request.headers:
                self.logger.log_blocked_request(request, f"Missing required header: {header}")
                abort(400, description=f"Missing required header: {header}")

    def _check_rate_limit(self):
        if self.rate_limiter.is_rate_limited(request.remote_addr):
            self.logger.log_blocked_request(request, "Rate limit exceeded")
            abort(429, description="Too many requests")

    def _check_threat_intelligence(self):
        if self.threat_intel.is_malicious(request):
            self.logger.log_blocked_request(request, "Threat intelligence match")
            abort(403, description="Request blocked by threat intelligence")

    def _check_anomalies(self):
        if self.anomaly_detection.is_anomalous(request):
            self.logger.log_blocked_request(request, "Anomalous behavior detected")
            abort(403, description="Request blocked due to anomalous behavior")

    def add_security_headers(self, response):
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        csp_header = self.csp.generate_csp_header()
        response.headers['Content-Security-Policy'] = csp_header

        return response

