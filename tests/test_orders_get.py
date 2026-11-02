import allure


@allure.feature("Получение заказов пользователя")
class TestOrdersGet:
    """Тесты для получения заказов пользователя"""

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, create_and_delete_user, test_ingredients, api_helpers):
        """Получение заказов авторизованным пользователем"""
        token = create_and_delete_user["access_token"]
        api_helpers.create_order(token, test_ingredients[:2])

        response = api_helpers.get_orders(token)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        assert "total" in response_data
        assert "totalToday" in response_data

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self, api_helpers):
        """Получение заказов без авторизации"""
        response = api_helpers.get_orders("")
        response_data = response.json()

        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == "You should be authorised"