import pytest
import requests

from faker import Faker
from constant import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username" : "admin", "password" : "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"
    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }
@pytest.fixture()
def  booking_data_put():
    return {
            "firstname":"hyi",
            "lastname": "pizda",
            "totalprice": 3500,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Breakfast"
        }

@pytest.fixture()
def new_booking(auth_session, booking_data):
    create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
    assert create_booking.status_code == 200, "Некорректный статус код"
    booking_id = create_booking.json().get("bookingid")
    assert booking_id is not None, "ID букинга не найден в ответе"
    get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
    assert get_booking.status_code == 200, "Созданная запись отсутствует в бд"

    return booking_id
