import re
from flask import request
import json

class Rule:
    def __init__(self, name, pattern, locations):
        self.name = name
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.locations = locations

    def check(self, data):
        return bool(self.pattern.search(data))

class RuleEngine:
    def __init__(self):
        self.rules = [
            Rule('SQL Injection', r'(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)(\s|$)', ['params', 'form', 'json']),
            Rule('XSS', r'<script.*?>|<.*?on\w+\s*=|javascript:', ['params', 'form', 'json']),
            Rule('Path Traversal', r'\.\.\/|\.\.\\|%2e%2e%2f|%2e%2e/', ['params', 'path']),
            Rule('Command Injection', r';\s*(\w+\s+)*(\w+)|\||\$\(|\`', ['params', 'form', 'json']),
            Rule('File Inclusion', r'\.\./|\.\.\\|file://', ['params', 'path']),
            Rule('HTTP Response Splitting', r'\r|\n', ['headers']),
        ]

    def check_request(self, req):
        violations = []

        for rule in self.rules:
            if 'params' in rule.locations and rule.check(str(req.args)):
                violations.append((rule.name, 'URL parameters'))
            if 'form' in rule.locations and rule.check(str(req.form)):
                violations.append((rule.name, 'Form data'))
            if 'json' in rule.locations and req.is_json:
                json_data = json.dumps(req.get_json())
                if rule.check(json_data):
                    violations.append((rule.name, 'JSON data'))
            if 'headers' in rule.locations and rule.check(str(req.headers)):
                violations.append((rule.name, 'Headers'))
            if 'path' in rule.locations and rule.check(req.path):
                violations.append((rule.name, 'URL path'))

        return violations

