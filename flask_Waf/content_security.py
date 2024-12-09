class ContentSecurityPolicy:
    def __init__(self):
        self.policies = {
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'img-src': ["'self'", "data:", "https:"],
            'font-src': ["'self'", "https:", "data:"],
            'connect-src': ["'self'"],
            'media-src': ["'self'"],
            'object-src': ["'none'"],
            'frame-src': ["'self'"],
            'base-uri': ["'self'"],
            'form-action': ["'self'"],
        }

    def add_policy(self, directive, source):
        if directive in self.policies:
            self.policies[directive].append(source)
        else:
            self.policies[directive] = [source]

    def generate_csp_header(self):
        return '; '.join(f"{key} {' '.join(value)}" for key, value in self.policies.items())

