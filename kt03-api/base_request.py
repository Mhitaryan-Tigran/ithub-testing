import time

import requests

BASE_URL_PETSTORE = "https://petstore.swagger.io/v2"


class BaseRequest:
    def __init__(self, base_url, retries=3, timeout=15):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
        self.retries = retries
        self.timeout = timeout
        self.log = []

    def _request(self, method, path, expected_status=200, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = None
        for attempt in range(1, self.retries + 1):
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            if response.status_code == expected_status or response.status_code < 500:
                break
            time.sleep(attempt)
        self.log.append(f"{method} {response.url} -> {response.status_code}")
        return response

    def eventually(self, path, check, attempts=6):
        body = None
        for attempt in range(attempts):
            response = self.get(path)
            body = response.json() if response.status_code == 200 else None
            if body is not None and check(body):
                return body
            time.sleep(0.5 * (attempt + 1))
        return body

    def get(self, path, expected_status=200, **kwargs):
        return self._request("GET", path, expected_status, **kwargs)

    def post(self, path, body=None, expected_status=200):
        return self._request("POST", path, expected_status, json=body)

    def put(self, path, body=None, expected_status=200):
        return self._request("PUT", path, expected_status, json=body)

    def delete(self, path, expected_status=200):
        return self._request("DELETE", path, expected_status)
