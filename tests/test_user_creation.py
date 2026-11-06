import time

import allure
import pytest

from data.test_data import TestData


@allure.feature("Создание пользователя")
class TestUserCreation:
    """Тесты для создания пользователя"""

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_helpers, cleanup_created_users):
        timestamp = int(time.time() * 1000)
        user_data = {
            "email": f"new_user_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"User_{timestamp}",
        }

        response = api_helpers.create_user(user_data)
        response_data = response.json()

        if response.status_code == 200:
            cleanup_created_users.append(response_data["accessToken"])

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_data["email"]
        assert response_data["user"]["name"] == user_data["name"]
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

    @allure.title("Создание пользователя, который уже существует")
    def test_create_existing_user(self, api_helpers, create_and_delete_user):
        existing_data = create_and_delete_user["data"]

        response = api_helpers.create_user(existing_data)
        response_data = response.json()

        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == TestData.ERROR_MESSAGES["user_exists"]

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_helpers, missing_field):
        timestamp = int(time.time() * 1000)
        user_data = {
            "email": f"test_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"User_{timestamp}",
        }
        del user_data[missing_field]

        response = api_helpers.create_user(user_data)
        response_data = response.json()

        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == TestData.ERROR_MESSAGES["required_fields"]