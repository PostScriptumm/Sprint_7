import requests
import random
import string
import pytest

from data import UrlData


# фикстура создания данных для регистрации курьера
@pytest.fixture
def create_courier_data():
    def generate_random_string(length):
        return ''.join((random.choice(string.ascii_lowercase + string.digits) for x in range(length)))
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {"login": login, "password": password, "firstName": first_name}
    return payload


# фикстура регистрации курьера
@pytest.fixture
def register_new_courier(create_courier_data):
    payload = create_courier_data
    response = requests.post(UrlData.url_create_courier, data=payload)
    return response


@pytest.fixture
def login_and_delete_courier(create_courier_data, register_new_courier):
    login_data = create_courier_data
    login_data.pop('firstName')
    response = requests.post(UrlData.url_login_courier, data=login_data)
    yield response
    id_courier = response.json()['id']
    requests.delete(f"{UrlData.url_delete_courier}/{id_courier}")
