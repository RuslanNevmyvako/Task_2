import time

import allure

from data.test_data import TestData


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    """Тесты для изменения данных пользователя"""

    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_user_email_with_auth(self, create_and_delete_user, api_helpers):
        token = create_and_delete_user["access_token"]
        timestamp = int(time.time() * 1000)
        new_email = f"updated_{timestamp}@test.com"

        response = api_helpers.update_user(token, {"email": new_email})
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["user"]["email"] == new_email

    @allure.title("Изменение имени пользователя с авторизацией")
    def test_update_user_name_with_auth(self, create_and_delete_user, api_helpers):
        token = create_and_delete_user["access_token"]
        timestamp = int(time.time() * 1000)
        new_name = f"UpdatedUser_{timestamp}"

        response = api_helpers.update_user(token, {"name": new_name})
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["user"]["name"] == new_name

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth(self, api_helpers):
        update_data = {
            "email": "unauthorized@test.com",
            "name": "Unauthorized",
        }

        response = api_helpers.update_user("", update_data)
        response_data = response.json()

        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == TestData.ERROR_MESSAGES["unauthorized"]