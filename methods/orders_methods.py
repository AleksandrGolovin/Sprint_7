import requests


class OrdersMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url

    def create_order(self, params):
        response = requests.post(
            url=self.namespace_url,
            json=params
        )
        return response