import json
import logging

import allure
import requests
from allure_commons.types import Severity
from jsonschema.validators import validate

from api_methods.api import base_url, booking_endpoint, CreateUpdateBook, auth_booking, response_logging
from models.schemas import schema_update_success

update_body = CreateUpdateBook()
auth_token = auth_booking()


@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка редактирования собственного заказа')
def test_update_self_book():
    response = requests.put(
        url=base_url + booking_endpoint + "21",
        headers={
            'Cookie': f'token={auth_token}'
        },
        json=update_body.create_update_body_valid(
            first_name="Petr",
            last_name="Petrov",
            total_price="900",
            depositpaid_bool="True",
            checkin_yyyy_mm_dd="2025-07-05",
            checkout_yyyy_mm_dd="2025-07-10",
            additional_needs="breakfast+dinner"
        )
    )
    assert response.status_code == 200
    assert json.loads(response.text)['additionalneeds'] == "breakfast+dinner"
    response_body = response.json()
    validate(response_body, schema_update_success)
    response_logging(response=response)


@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка редактирования несуществующего заказа')
def test_update_non_existent_book():
    response = requests.put(
        url=base_url + booking_endpoint + "214546184",
        headers={
            'Cookie': f'token={auth_token}'
        },
        json=update_body.create_update_body_valid(
            first_name="Petr123",
            last_name="Petrov123",
            total_price="900123",
            depositpaid_bool="True",
            checkin_yyyy_mm_dd="2025-07-05",
            checkout_yyyy_mm_dd="2025-07-10",
            additional_needs="breakfast+dinner"
        )
    )
    assert response.status_code == 405
    response_logging(response=response)


@allure.severity(Severity.NORMAL)
@allure.tag("API")
@allure.label("owner", "Xeniy4")
@allure.suite("API-Тесты")
@allure.title('Проверка редактирования с невалидными данными, например, без поля firstname')
def test_update_non_existent_book():
    response = requests.put(
        url=base_url + booking_endpoint + "21454618416846165",
        headers={
            'Cookie': f'token={auth_token}'
        },
        json=update_body.create_update_body_no_firstname(
            last_name="Petrov321",
            total_price="900321",
            depositpaid_bool="True",
            checkin_yyyy_mm_dd="2025-07-05",
            checkout_yyyy_mm_dd="2025-07-10",
            additional_needs="breakfast+dinner"
        )
    )
    assert response.status_code == 400
    response_logging(response=response)
