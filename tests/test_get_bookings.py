import logging

import allure
import requests
from allure_commons.types import Severity
from jsonschema.validators import validate

from api_methods.api import base_url, CreateUpdateBook, booking_endpoint, GetBooks, response_logging
from models.schemas import schema_get_book

create_book = CreateUpdateBook()
id_book = create_book.create_valid_booking()
id_book = str(id_book)
get_book = GetBooks()


@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка поиска ранее созданного нами заказа')
def test_get_booking_ids_from_create_book():
    create_book.create_valid_booking()
    response = requests.get(
        url=base_url + booking_endpoint + id_book
    )
    assert response.status_code == 200
    response_body = response.json()
    validate(response_body, schema_get_book)
    response_logging(response=response)


@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка поиска существующего заказа, id = 3')
def test_get_random_booking_ids():
    response_get = get_book.get_booking_with_id(3)
    assert response_get.status_code == 200
    response_body = response_get.json()
    validate(response_body, schema_get_book)
    response_logging(response=response_get)



@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка поиска несуществующего заказа, id = 123456789123')
def test_gen_non_existent_id():
    response_get = get_book.get_booking_with_id(123456789123)
    assert response_get.status_code == 404
    response_logging(response=response_get)
