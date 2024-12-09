## Flask-WAF

Flask-WAF is an advanced Web Application Firewall (WAF) extension for Flask applications. It provides comprehensive protection against various web application threats, enhancing the security of your Flask-based web applications.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Advanced Usage](#advanced-usage)
6. [License](#license)

## Features

- Advanced rule engine for detecting and blocking malicious requests
- Session protection to prevent session hijacking and fixation attacks
- Content Security Policy (CSP) implementation
- Threat intelligence integration
- Anomaly detection to identify unusual patterns
- Rate limiting to prevent abuse
- Comprehensive logging
- Customizable security rules and policies

## Installation

You can install Flask-WAF using pip:

```bash
pip install flask-waf
```

Alternatively, you can install from the source:

```shellscript
git clone https://github.com/yourusername/flask-waf.git
cd flask-waf
pip install -e .
```

## Quick Start

Here's a simple example of how to use Flask-WAF:

```python
from flask import Flask
from flask_waf import WAF

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for session handling
waf = WAF(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

This basic setup will apply default WAF protection to your Flask application.

## Configuration

Flask-WAF can be configured using a JSON file or by passing a dictionary to the WAF constructor. Here's an example configuration:

```python
waf_config = {
    "max_request_size": 1048576,  # 1MB
    "allowed_content_types": [
        "application/x-www-form-urlencoded",
        "application/json",
        "multipart/form-data"
    ],
    "max_url_length": 2083,
    "max_query_params": 100,
    "max_headers": 100,
    "required_headers": ["Host", "User-Agent"],
    "rate_limit": 100,  # requests per minute
    "session_protection": True,
    "content_security_policy": {
        "default-src": ["'self'"],
        "script-src": ["'self'", "'unsafe-inline'"],
        "style-src": ["'self'", "'unsafe-inline'"],
    },
    "anomaly_detection": {
        "request_threshold": 10,
        "time_window": 60
    }
}

waf = WAF(app, config=waf_config)
```

You can also load the configuration from a JSON file:

```python
waf = WAF(app, config_file='waf_config.json')
```

## Advanced Usage

### Custom Rules

You can add custom rules to the WAF's rule engine:

```python
from flask_waf import WAF, Rule

waf = WAF(app)

custom_rule = Rule(
    name='Custom SQL Injection Check',
    pattern=r'UNION\s+SELECT',
    locations=['params', 'form', 'json'],
    severity='high',
    description='Detected potential SQL injection attempt'
)

waf.rule_engine.add_rule(custom_rule)
```

### Threat Intelligence Integration

You can update the threat intelligence module with custom malicious patterns:

```python
waf.threat_intel.add_malicious_pattern(r'malware\.com')
waf.threat_intel.add_malicious_ip_range('192.0.2.0', '192.0.2.255')
```

### Logging

Flask-WAF provides comprehensive logging. You can customize the log file location:

```python
waf.logger.set_log_file('/path/to/waf.log')
```

## API Reference

### WAF Class

The main class for initializing the Web Application Firewall.

```python
class WAF:
    def __init__(self, app=None, config=None, config_file=None):
        ...

    def init_app(self, app):
        ...

    def check_request(self):
        ...

    def add_security_headers(self, response):
        ...
```

### Rule Class

Used for defining custom security rules.

```python
class Rule:
    def __init__(self, name, pattern, locations, severity='medium', description=''):
        ...

    def check(self, data):
        ...
```

### RuleEngine Class

Manages and applies security rules.

```python
class RuleEngine:
    def add_rule(self, rule):
        ...

    def remove_rule(self, rule_name):
        ...

    def check_request(self, request):
        ...
```

## License

Flask-WAF is released under the MIT License. See the [LICENSE](LICENSE) file for more details.
