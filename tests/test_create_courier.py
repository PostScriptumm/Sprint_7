import allure
import requests
import pytest
import random
import string

from data import UrlData
from conftest import create_courier_data, login_and_delete_courier, register_new_courier


class TestCreateCourier:

    @allure.title('Проверка возвращаемого кода 201 при успешном создании курьера')
    def test_status_code_201(self, register_new_courier, login_and_delete_courier):
        response = register_new_courier
        assert response.status_code == 201

    @allure.title('Проверка текста в теле ответа при успешном создании курьера')
    def test_text_of_body_successful_request(self, register_new_courier, login_and_delete_courier):
        response = register_new_courier
        assert response.text == '{"ok":true}'

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с уже существующими данными')
    def test_create_same_courier_data(self, create_courier_data, login_and_delete_courier):
        payload = create_courier_data
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 409 and response.json()["message"] == 'Этот логин уже используется'

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с уже существующим логином')
    def test_create_same_courier_login(self, register_new_courier, create_courier_data):
        payload = create_courier_data
        payload['password'] = ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(10)))
        payload['firstName'] = ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(10)))
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 409 and response.json()["message"] == 'Этот логин уже используется'

    @allure.title('Проверка возвращаемого кода 409 при создании курьера c пустыми обязательными полями')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_null_login_or_password(self, create_courier_data, item):
        payload = create_courier_data
        payload[item] = ''
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 400 \
               and response.json()["message"] == 'Недостаточно данных для создания учетной записи'

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с отсутсвующими обязательными полями')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_without_login_or_password(self, create_courier_data, item):
        payload = create_courier_data
        payload.pop(item)
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 400 \
               and response.json()["message"] == 'Недостаточно данных для создания учетной записи'
