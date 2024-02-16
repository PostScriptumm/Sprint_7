import allure
import pytest
import requests

from data import UrlData, ResponseBodyText
from helpers import Helper
from conftest import create_courier_data, login_and_delete_courier, register_new_courier


class TestAuthCourier:

    @allure.title('Проверка возвращаемого кода 201 и наличия id в теле ответа при успешном логине курьера')
    def test_successful_login_courier(self, login_and_delete_courier):
        response = login_and_delete_courier
        response_body = response.json()
        assert response.status_code == 200 and 'id' in response_body.keys()

    @allure.title('Проверка возвращаемого кода 404 при логине несуществующим курьером')
    def test_login_nonexistent_courier(self):
        login_data = {'login': Helper.generate_random_string(10), 'password': Helper.generate_random_string(10)}
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 404 and response.json()["message"] == ResponseBodyText.account_not_found

    @allure.title('Проверка возвращаемого кода 400 при логине с отсутствующими полями логина или пароля')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_login_courier_without_login_or_password(self, item, create_courier_data, login_and_delete_courier):
        login_data = create_courier_data
        login_data.pop(item)
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 400 and response.json()["message"] == ResponseBodyText.no_login_information

    @allure.title('Проверка возвращаемого кода 404 при логине с неправильными логином или паролем')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_login_courier_fail_login_or_password(self, item, create_courier_data, login_and_delete_courier):
        login_data = create_courier_data
        login_data[item] = 'abcd'
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 404 and response.json()["message"] == ResponseBodyText.account_not_found
