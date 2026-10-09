import requests


class ApiSession(requests.Session):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, path, **kwargs):
        return super().request(method, f"{self.base_url}{path}", **kwargs)
