import pytest
from methods.courier_methods import CourierMethods
import helpers


class TestCreateCourier:
    # Создание курьера с уникальными данными - 201 (created) + ok message
    def test_create_courier_unique_data_created_ok_message(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()
        ok_message = '{"ok":true}'

        response = courier_methods.create_courier(params)

        assert response.status_code == 201 and response.text == ok_message
    
    # Создание курьера с неуникальными данными (попытка повторного создания) - 409 (conflict) + error message
    def test_create_courier_nonunique_data_conflict_error_message(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()
        error_message = 'Этот логин уже используется. Попробуйте другой.'

        response_unique = courier_methods.create_courier(params)
        response_nonunique = courier_methods.create_courier(params)

        assert response_unique.status_code == 201 and response_nonunique.status_code == 409 and response_nonunique.json()['message'] == error_message

    # Создание курьера с неполными учетными данными - 400 (bad request) + error message
    @pytest.mark.parametrize("params", 
        [
            {"password": "pass123", "firstName": "First Name"},
            {"login": "log123", "firstName": "First Name"},
            {"firstName": "First Name"}
        ]
    )
    def test_create_courier_incomplete_data_bad_request_error_message(self, params, courier_methods: CourierMethods):
        error_message = 'Недостаточно данных для создания учетной записи'
        
        response = courier_methods.create_courier(params)

        assert response.status_code == 400 and response.json()['message'] == error_message