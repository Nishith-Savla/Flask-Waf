import json

class WAFConfig:
    def __init__(self):
        self.max_request_size = 1024 * 1024  # 1 MB
        self.allowed_content_types = [
            'application/x-www-form-urlencoded',
            'application/json',
            'multipart/form-data'
        ]
        self.max_url_length = 2083  # Common max URL length
        self.max_query_params = 100
        self.max_headers = 100
        self.required_headers = ['Host', 'User-Agent']
        self.blocked_countries = []  # List of country codes to block
        self.rate_limit = 100  # Requests per minute
        self.geoip_database_path = 'path/to/geoip/database'

    def load_from_file(self, config_file):
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save_to_file(self, config_file):
        config_data = {key: value for key, value in self.__dict__.items() if not key.startswith('__')}
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

