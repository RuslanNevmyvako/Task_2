import pytest
import allure
import time
from helpers.api_helpers import ApiHelpers

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.feature("Создание пользователя")
class TestUserCreation:
    """Тесты для создания пользователя"""
    
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_helpers):
        """Тест создания уникального пользователя - полностью независимый"""
        timestamp = int(time.time() * 1000)
        user_data = {
            "email": f"test_{timestamp}_{hash(time.time()) % 10000}@test.com",
            "password": f"Pass{timestamp}123!",
            "name": f"User_{timestamp % 10000}"
        }
        
        response = api_helpers.create_user(user_data)
        
        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["user"]["email"] == user_data["email"]
        assert response_data["user"]["name"] == user_data["name"]
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
    
    @allure.title("Создание пользователя, который уже существует")
    def test_create_existing_user(self, create_and_delete_user, api_helpers):
        """Тест создания пользователя, который уже зарегистрирован"""
        existing_data = create_and_delete_user["data"]
        
        response = api_helpers.create_user(existing_data)
        
        # Проверяем код ответа
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == "User already exists"
    
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_helpers, missing_field):
        """Тест создания пользователя без одного из обязательных полей"""
        timestamp = int(time.time())
        user_data = {
            "email": f"test_{timestamp}@test.com",
            "password": "TestPass123!",
            "name": f"User_{timestamp}"
        }
        
        # Удаляем одно из полей
        del user_data[missing_field]
        
        response = api_helpers.create_user(user_data)
        
        # Проверяем код ответа
        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is False
        assert "Email, password and name are required fields" in response_data["message"]