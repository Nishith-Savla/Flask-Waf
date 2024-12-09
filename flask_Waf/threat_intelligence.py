import re

class ThreatIntelligence:
    def __init__(self):
        self.malicious_ip_ranges = [
            ('192.0.2.0', '192.0.2.255'),  # Example range, replace with actual threat intel
        ]
        self.malicious_patterns = [
            r'malware\.com',
            r'evil\.org',
        ]

    def is_malicious(self, request):
        ip = request.remote_addr
        if self._is_ip_in_range(ip):
            return True

        url = request.url
        user_agent = request.headers.get('User-Agent', '')
        if self._match_patterns(url) or self._match_patterns(user_agent):
            return True

        return False

    def _is_ip_in_range(self, ip):
        ip_parts = list(map(int, ip.split('.')))
        for start, end in self.malicious_ip_ranges:
            start_parts = list(map(int, start.split('.')))
            end_parts = list(map(int, end.split('.')))
            if start_parts <= ip_parts <= end_parts:
                return True
        return False

    def _match_patterns(self, text):
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in self.malicious_patterns)

