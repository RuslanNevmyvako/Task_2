import pytest
import allure
from helpers.api_helpers import ApiHelpers

BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.feature("Получение заказов пользователя")
class TestOrdersGet:
    """Тесты для получения заказов пользователя"""
    
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, create_and_delete_user, test_ingredients, api_helpers):
        """Тест получения заказов авторизованного пользователя - полностью независимый"""
        token = create_and_delete_user["access_token"]
        
        # Сначала создаем заказ
        order_response = api_helpers.create_order(token, test_ingredients[:2])
        assert order_response.status_code == 200, f"Не удалось создать заказ: {order_response.text}"
        
        # Получаем заказы
        response = api_helpers.get_orders(token)
        
        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is True
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        assert "total" in response_data
        assert "totalToday" in response_data
        
        # Проверяем, что заказ есть
        assert len(response_data["orders"]) > 0, "Нет заказов у пользователя"
        order = response_data["orders"][0]
        assert "ingredients" in order
        assert "_id" in order
        assert "status" in order
        assert "number" in order
    
    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self, api_helpers):
        """Тест получения заказов неавторизованного пользователя"""
        response = api_helpers.get_orders("")
        
        # Проверяем код ответа
        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is False
        assert "You should be authorised" in response_data["message"]