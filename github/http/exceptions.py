class HTTPRequestError:
    def __init__(self, message=None, response=None):
        self.message = message
        self.response = response

    def get_status_code(self):
        return self.response.status_code if self.response else None

    def get_response_json(self):
        if self.response and self.response.headers.get('content-type', '').startswith('application/json'):
            return self.response.json()
        return None

    def __str__(self):
        return self.message