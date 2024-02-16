class UrlData:

    # Авторизация курьера POST
    url_login_courier = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'

    # Создание курьера POST
    url_create_courier = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'

    # Удаление курьера DELETE
    url_delete_courier = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/'

    # Создание заказа POST
    url_create_order = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

    # Получение списка заказов GET
    url_get_order_list = 'https://qa-scooter.praktikum-services.ru/api/v1/orders?courierId='

    # Принятие заказа PUT
    url_accept_order = 'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept'

    # Получение заказа по номеру GET
    url_get_order = 'https://qa-scooter.praktikum-services.ru/api/v1/orders/track'


class OrderData:

    # данные для создания заказа
    order_data = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": [
            "BLACK"
        ]
    }

    # варианты для поля color
    color_list = ['BLACK', 'GREY', 'BLACK, GREY', '']


class ResponseBodyText:

    account_not_found = 'Учетная запись не найдена'
    no_login_information = "Недостаточно данных для входа"
    no_information_to_account = 'Недостаточно данных для создания учетной записи'
    used_login = 'Этот логин уже используется'
