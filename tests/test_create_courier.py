import allure
import requests
import pytest

from data import UrlData, ResponseBodyText
from helpers import Helper
from conftest import create_courier_data, login_and_delete_courier, register_new_courier


class TestCreateCourier:

    @allure.title('Проверка возвращаемого кода 201 и текста в теле ответа при успешном создании курьера')
    def test_successful_registration_courier(self, register_new_courier, login_and_delete_courier):
        response = register_new_courier
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с уже существующими данными')
    def test_create_same_courier_data(self, create_courier_data, login_and_delete_courier):
        payload = create_courier_data
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 409 and response.json()["message"] == ResponseBodyText.used_login

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с уже существующим логином')
    def test_create_same_courier_login(self, register_new_courier, create_courier_data):
        payload = create_courier_data
        payload['password'] = Helper.generate_random_string(10)
        payload['firstName'] = Helper.generate_random_string(10)
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 409 and response.json()["message"] == ResponseBodyText.used_login

    @allure.title('Проверка возвращаемого кода 409 при создании курьера c пустыми обязательными полями')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_null_login_or_password(self, create_courier_data, item):
        payload = create_courier_data
        payload[item] = ''
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 400 and response.json()["message"] == ResponseBodyText.no_information_to_account

    @allure.title('Проверка возвращаемого кода 409 при создании курьера с отсутсвующими обязательными полями')
    @pytest.mark.parametrize('item', ['login', 'password'])
    def test_create_courier_without_login_or_password(self, create_courier_data, item):
        payload = create_courier_data
        payload.pop(item)
        response = requests.post(UrlData.url_create_courier, data=payload)
        assert response.status_code == 400 and response.json()["message"] == ResponseBodyText.no_information_to_account
