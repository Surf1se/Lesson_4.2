from conftest import new_booking
from constant import BASE_URL
from datetime import date
from pydantic import BaseModel
from booking_api import BookingApi

class BookingDates(BaseModel):
    checkin: date
    checkout: date

class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str


class TestBookings:

    booking_api = BookingApi(BASE_URL)

    """ ---------- Happy PASSED ---------- """
    """ Проверяем рабоатет ли сревер пеперед тестом """
    def test_get_check_ping(self,auth_session, new_booking):
        check = auth_session.get(f"{BASE_URL}/ping")
        assert check.status_code == 201, "Сервер не ответил, тест окончен"

    """ CREATE """
    def test_create_booking(self, auth_session, booking_data):
        booking_id = TestBookings.booking_api.post_booking(auth_session, booking_data)

        get_booking = TestBookings.booking_api.get_booking(auth_session, booking_id)

        validated_booking = Booking(**get_booking)

        assert validated_booking.firstname == booking_data['firstname'], "Имя не совпадает с заданным"
        assert validated_booking.lastname == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert validated_booking.totalprice == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert validated_booking.depositpaid == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert validated_booking.bookingdates.checkin == date.fromisoformat(
            booking_data['bookingdates']['checkin']), "Дата заезда не совпадает"
        assert validated_booking.bookingdates.checkout == date.fromisoformat(
            booking_data['bookingdates']['checkout']), "Дата выезда не совпадает"

        TestBookings.booking_api.delete_booking(auth_session, booking_id)

    """ PATCH """
    def test_patch_booking(self, auth_session, booking_data, new_booking):
        booking_id = new_booking

        booking_data_patch = {
            "firstname" : "Surf1se"
        }

        new_bookingData_response = TestBookings.booking_api.patch_booking(auth_session, booking_id,booking_data_patch)
        assert new_bookingData_response["firstname"] != booking_data["firstname"], "Имя не обновилось"

        TestBookings.booking_api.delete_booking(auth_session, booking_id)

    """ PUT """
    def test_put_booking(self, auth_session, booking_data, new_booking, booking_data_put):
        booking_id = new_booking

        new_bookingData_response = TestBookings.booking_api.put_booking(auth_session, booking_id, booking_data_put)
        assert new_bookingData_response["firstname"] != booking_data["firstname"], "Имя не обновилось"

        TestBookings.booking_api.delete_booking(auth_session, booking_id)

    """ GET """
    def test_get_bookings(self, auth_session):
        count_getBooking = TestBookings.booking_api.get_bookings(auth_session)
        assert len(count_getBooking) > 0, "Список бронирований пуст"

        """Конструкция для проверки наличия ключа в теле ответа"""
        search_key = any("bookingid" in i for i in count_getBooking)
        assert search_key is True, "Get не имеет атрибута bookingid"

    """ ---------- FAILED ---------- """
    """ Тут нету проверки от бэка на корректность заполнения (например : firstname должно быть str)"""
    def test_fail_patch(self, auth_session, new_booking):
        booking_id = new_booking

        booking_data = {
            "firstname": 123
        }

        new_bookingData = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert new_bookingData.status_code == 400, f"patch отрабортал"

        TestBookings.booking_api.delete_booking(auth_session, booking_id)

    """Проверка  параметра 'lastname' на обязательность"""
    def test_fail_post (self, auth_session, booking_data):
        booking_data_copy = booking_data.copy()
        del booking_data_copy["lastname"]

        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data_copy)
        assert create_booking.status_code == 500, "Бронь создается без указания обязательного параметра"