import requests
from github.http.exceptions import HTTPRequestError

class HTTPClient:
    def __init__(self, base_url=None, headers=None, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs['timeout'] = self.timeout
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise HTTPRequestError(f"HTTP request failed: {str(e)}", response=e.response)

    def get(self, endpoint, params=None):
        response = self._make_request('GET', endpoint, params=params)
        return response.json()

    def post(self, endpoint, data=None, json=None):
        response = self._make_request('POST', endpoint, data=data, json=json)
        return response.json()

    def put(self, endpoint, data=None, json=None):
        response = self._make_request('PUT', endpoint, data=data, json=json)
        return response.json()

    def delete(self, endpoint):
        self._make_request('DELETE', endpoint)

    def patch(self, endpoint, data=None, json=None):
        response = self._make_request('PATCH', endpoint, data=data, json=json)
        return response.json()