from conftest import booking_data
from constant import BASE_URL
from constant import HEADERS


class BookingApi:

    def __init__(self, base_url):
        self.base_url = base_url

    def get_bookings(self, auth_session):
        get_booking = auth_session.get(f"{BASE_URL}/booking")
        assert get_booking.status_code == 200, f"GET /booking завершился неудачно с кодом состояния: {get_booking.status_code}"
        return get_booking.json()

    def get_booking(self, auth_session, booking_id):
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200
        return get_booking.json()

    def post_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID букинга не найден в ответе"
        return booking_id

    def put_booking(self, auth_session, booking_id, booking_data_put):
        new_bookingData = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data_put)
        assert new_bookingData.status_code == 200, f"put не отрабортал"
        return new_bookingData.json()

    def patch_booking(self, auth_session, booking_id,booking_data_patch):
        new_bookingData = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data_patch)
        assert new_bookingData.status_code == 200, "patch не отработал"
        return new_bookingData.json()

    def delete_booking(self, auth_session, booking_id):
        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Букинг с ID : {booking_id} не удалился успешно. Статус код: {delete_booking.status_code}"
