import hashlib
from flask import session

class SessionProtection:
    def __init__(self):
        self.secret_key = 'your-secret-key'  # In production, use a secure random key

    def validate_session(self, request):
        if 'user_id' not in session:
            return False

        expected_hash = self._generate_session_hash(request)
        return session.get('session_hash') == expected_hash

    def set_session_data(self, request):
        session['session_hash'] = self._generate_session_hash(request)

    def _generate_session_hash(self, request):
        user_agent = request.headers.get('User-Agent', '')
        ip_address = request.remote_addr
        user_id = session.get('user_id', '')

        hash_input = f"{user_agent}{ip_address}{user_id}{self.secret_key}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

