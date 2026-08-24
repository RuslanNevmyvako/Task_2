import pytest
import allure
from helpers.api_helpers import ApiHelpers

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.feature("Создание заказа")
class TestOrdersCreation:
    """Тесты для создания заказа"""
    
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, create_and_delete_user, test_ingredients, api_helpers):
        """Тест создания заказа с авторизацией"""
        
        assert create_and_delete_user is not None, "Пользователь не создан"
        
        token = create_and_delete_user["access_token"]
        assert token is not None, "Токен не получен"
        assert len(token) > 0, "Токен пустой"
        
        assert test_ingredients is not None, "Ингредиенты не получены"
        assert len(test_ingredients) > 0, "Нет ингредиентов"
        
        ingredients = test_ingredients[:2]
        print(f"🟢 Создаем заказ с ингредиентами: {ingredients}")
        
        response = api_helpers.create_order(token, ingredients)
        
        # Вместо pytest.skip - выбрасываем AssertionError
        assert response is not None, "Ответ от сервера не получен (None). Сервер API недоступен."
        
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert response_data["order"]["number"] is not None
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, test_ingredients, api_helpers):
        """Тест создания заказа без авторизации"""
        
        assert test_ingredients is not None, "Ингредиенты не получены"
        assert len(test_ingredients) > 0, "Нет ингредиентов"
        
        ingredients = test_ingredients[:2]
        response = api_helpers.create_order(None, ingredients)
        
        assert response is not None, "Ответ от сервера не получен (None). Сервер API недоступен."
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert response_data["order"]["number"] is not None
    
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, create_and_delete_user, test_ingredients, api_helpers):
        """Тест создания заказа с ингредиентами"""
        
        assert create_and_delete_user is not None, "Пользователь не создан"
        
        token = create_and_delete_user["access_token"]
        assert token is not None, "Токен не получен"
        
        assert test_ingredients is not None, "Ингредиенты не получены"
        assert len(test_ingredients) > 0, "Нет ингредиентов"
        
        response = api_helpers.create_order(token, test_ingredients)
        
        assert response is not None, "Ответ от сервера не получен (None). Сервер API недоступен."
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert response_data["success"] is True
        assert "name" in response_data
        assert "order" in response_data
        assert response_data["order"]["number"] is not None
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user, api_helpers):
        """Тест создания заказа без ингредиентов"""
        
        assert create_and_delete_user is not None, "Пользователь не создан"
        
        token = create_and_delete_user["access_token"]
        assert token is not None, "Токен не получен"
        
        response = api_helpers.create_order(token, [])
        
        assert response is not None, "Ответ от сервера не получен (None). Сервер API недоступен."
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == "Ingredient ids must be provided"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient(self, create_and_delete_user, api_helpers):
        """Тест создания заказа с неверным хешем ингредиентов"""
        
        assert create_and_delete_user is not None, "Пользователь не создан"
        
        token = create_and_delete_user["access_token"]
        assert token is not None, "Токен не получен"
        
        invalid_ingredients = ["invalid_hash_123"]
        response = api_helpers.create_order(token, invalid_ingredients)
        
        assert response is not None, "Ответ от сервера не получен (None). Сервер API недоступен."
        assert response.status_code == 500, f"Ожидался 500, получен {response.status_code}. Ответ: {response.text}"