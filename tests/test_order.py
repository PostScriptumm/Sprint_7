import allure
import pytest
import requests
import json

from data import UrlData, OrderData
from conftest import create_courier_data, login_and_delete_courier, register_new_courier


class TestOrder:

    @allure.title('Проверка успешности создания заказа, при указании цветов из списка')
    @pytest.mark.parametrize('color', OrderData.color_list)
    def test_add_color_in_order(self, color):
        order_data = OrderData.order_data
        order_data['color'] = color
        order_data = json.dumps(OrderData.order_data)
        response = requests.post(UrlData.url_create_order, data=order_data)
        response_body = response.json()
        assert response.status_code == 201 and 'track' in response_body.keys()

    @allure.title('Проверка получения списка заказов курьера')
    def test_order_list(self, login_and_delete_courier):
        login = login_and_delete_courier
        create_order = requests.post(UrlData.url_create_order, data=json.dumps(OrderData.order_data))
        get_order = requests.get(f"{UrlData.url_get_order}?t={create_order.json()['track']}")
        requests.put(f"{UrlData.url_accept_order}/{get_order.json()['order']['id']}?courierId={login.json()['id']}")
        get_order_list = requests.get(f"{UrlData.url_get_order_list}{login.json()['id']}")
        assert get_order_list.json()['orders'][0]['id'] == get_order.json()['order']['id']
