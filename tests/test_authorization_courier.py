import allure
import pytest
import requests
import random
import string

from data import UrlData
from conftest import create_courier_data, login_and_delete_courier, register_new_courier


class TestAuthCourier:

    @allure.title('Проверка возвращаемого кода 201 при успешном логине курьера')
    def test_status_code_200(self, login_and_delete_courier):
        response = login_and_delete_courier
        assert response.status_code == 200

    @allure.title('Проверка наличия id в теле ответа при успешном логине курьера')
    def test_id_in_response(self, login_and_delete_courier):
        response = login_and_delete_courier
        response_body = response.json()
        assert 'id' in response_body.keys()

    @allure.title('Проверка возвращаемого кода 404 при логине несуществующим курьером')
    def test_login_nonexistent_courier(self):
        login_data = {'login': ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(10))),
                      'password': ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(10)))}
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 404 and response.json()["message"] == 'Учетная запись не найдена'

    @allure.title('Проверка возвращаемого кода 400 при логине с отсутствующими полями логина или пароля')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_without_login_or_password(self, item, create_courier_data, register_new_courier):
        login_data = create_courier_data
        login_data.pop('firstName')
        login = requests.post(UrlData.url_login_courier, data=login_data)
        login_data.pop(item)
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 400 and response.json()["message"] == 'Недостаточно данных для входа'
        requests.delete(f"{UrlData.url_delete_courier}/{login.json()['id']}")

    @allure.title('Проверка возвращаемого кода 404 при логине с неправильными логином или паролем')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_without_login_or_password(self, item, create_courier_data, register_new_courier):
        login_data = create_courier_data
        login_data.pop('firstName')
        login = requests.post(UrlData.url_login_courier, data=login_data)
        login_data[item] = 'abcd'
        response = requests.post(UrlData.url_login_courier, data=login_data)
        assert response.status_code == 404 and response.json()["message"] == 'Учетная запись не найдена'
        requests.delete(f"{UrlData.url_delete_courier}/{login.json()['id']}")
