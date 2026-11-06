import allure
import pytest

from data.test_data import TestData


@allure.feature("Логин пользователя")
class TestUserLogin:
    """Тесты для логина пользователя"""

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, api_helpers, create_and_delete_user):
        user_data = create_and_delete_user["data"]

        login_data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        response = api_helpers.login_user(login_data)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_data["email"]
        assert response_data["user"]["name"] == user_data["name"]
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

    @allure.title("Логин с неверным логином и паролем")
    @pytest.mark.parametrize("email, password", [
        ("wrong@email.com", "wrongpassword"),
        ("test@email.com", "wrongpassword"),
    ])
    def test_login_invalid_credentials(self, api_helpers, email, password):
        login_data = {
            "email": email,
            "password": password,
        }

        response = api_helpers.login_user(login_data)
        response_data = response.json()

        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == TestData.ERROR_MESSAGES["invalid_credentials"]