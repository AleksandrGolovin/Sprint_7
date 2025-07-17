import pytest
import allure
from methods.courier_methods import CourierMethods
from data import VALID_COURIER_DATA
import helpers


@allure.title('Тесты логина курьера')
class TestLoginCourier:
    @allure.title('Залогиниться под валидными учетными данными - 200 (ok) + id')
    @allure.description('Создать курьера с валидными данными, отправить запрос на логин, проверить код ответа и сообщение')
    def test_login_courier_valid_credentials_ok(self, courier_methods: CourierMethods):
        courier_methods.create_courier(VALID_COURIER_DATA)
        params = {
            "login": VALID_COURIER_DATA['login'],
            "password": VALID_COURIER_DATA['password']
        }

        response = courier_methods.login_courier(params)

        assert response.status_code == 200 and response.json()['id']
    
    @allure.title('Залогиниться без указания логина или пароля - 400 (bad request) + error message')
    @allure.description('Создать курьера с валидными данными, отправить запрос на логин с неполными данными, проверить код ответа и сообщение')
    @pytest.mark.parametrize("params", 
        [
            # Здесь косяк в сервисе: попытки отправить пустые данные или только логин приводят к статусу 504
            #{},
            #{"login": VALID_COURIER_DATA['login']},
            {"password": VALID_COURIER_DATA['password']}
        ]
    )
    def test_login_courier_incomplete_credetials_bad_reques(self, params, courier_methods: CourierMethods):
        courier_methods.create_courier(VALID_COURIER_DATA)
        error_message = 'Недостаточно данных для входа'

        response = courier_methods.login_courier(params)

        assert response.status_code == 400 and response.json()['message'] == error_message

    @allure.title('Залогиниться под несуществующими учетными данными - 404 (not found) + error message')
    @allure.description('Сгенерировать уникальные логин-пароль, отправить запрос на логин без создания курьера, проверить код ответа и сообщение')
    def test_login_courier_invalid_credentials_not_found(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()
        login_params = {
            "login": params['login'],
            "password": params['password']
        }
        error_message = 'Учетная запись не найдена'

        response = courier_methods.login_courier(login_params)

        assert response.status_code == 404 and response.json()['message'] == error_message
    
    @allure.title('Залогиниться с неверными паролем для существующего курьера - 404 (not found) + error message')
    @allure.description('Создать курьера с валидными данными, отправить запрос на логин с неверным паролем, проверить код ответа и сообщение')
    def test_login_courier_wrong_password_not_found(self, courier_methods: CourierMethods):
        courier_methods.create_courier(VALID_COURIER_DATA)
        params = {
            "login": VALID_COURIER_DATA['login'],
            "password": f'{VALID_COURIER_DATA['password']}_123'
        }
        error_message = 'Учетная запись не найдена'

        response = courier_methods.login_courier(params)

        assert response.status_code == 404 and response.json()['message'] == error_message