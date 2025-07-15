import pytest
import helpers
from methods.courier_methods import CourierMethods
from data import BASE_URL, COURIER_URL


@pytest.fixture
def courier_methods() -> CourierMethods:
    courier_namespace_url = f'{BASE_URL}{COURIER_URL}'
    courier_methods = CourierMethods(courier_namespace_url)
    return courier_methods

@pytest.fixture
def authorized_courier(courier_methods: CourierMethods):
    create_params = helpers.generate_courier_data()
    create_response = courier_methods.create_courier(create_params)
    if create_response.status_code == 201:
        login_params = {
            "login": create_params['login'],
            "password": create_params['password']
        }
        login_response = courier_methods.login_courier(login_params)
        yield login_response
    else:
        raise Exception('Что-то пошло не так, проверьте параметры запроса')
    delete_params = {'id': login_response.json()['id']}
    courier_methods.delete_courier(delete_params)
