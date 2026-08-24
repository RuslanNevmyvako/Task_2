import pytest
import allure
from helpers.api_helpers import ApiHelpers

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.feature("Логин пользователя")
class TestUserLogin:
    """Тесты для логина пользователя"""
    
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, create_and_delete_user, api_helpers):
        """Тест логина существующего пользователя"""
        user_data = create_and_delete_user["data"]
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = api_helpers.login_user(login_data)
        
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        response_data = response.json()
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
        """Тест логина с неверными данными"""
        login_data = {
            "email": email,
            "password": password
        }
        
        response = api_helpers.login_user(login_data)
        
        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
        
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == "email or password are incorrect"