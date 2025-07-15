import requests


class CourierMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url

    def create_courier(self, params):
        response = requests.post(
            url=self.namespace_url,
            data=params
        )
        return response

    def delete_courier(self, params):
        id = params.get('id', '')
        response = requests.delete(
            url=f'{self.namespace_url}/{id}',
            data=params
        )
        return response
    
    def login_courier(self, params):
        response = requests.post(
            url=f'{self.namespace_url}/login',
            data=params,
            timeout=10
        )
        return response