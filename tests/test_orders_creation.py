import allure

from data.test_data import TestData


@allure.feature("Создание заказа")
class TestOrdersCreation:
    """Тесты для создания заказа"""

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, create_and_delete_user, test_ingredients, api_helpers):
        token = create_and_delete_user["access_token"]
        ingredients = test_ingredients[:2]

        response = api_helpers.create_order(token, ingredients)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["name"]
        assert response_data["order"]["number"] is not None

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, test_ingredients, api_helpers):
        ingredients = test_ingredients[:2]

        response = api_helpers.create_order(None, ingredients)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["name"]
        assert response_data["order"]["number"] is not None

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, create_and_delete_user, test_ingredients, api_helpers):
        token = create_and_delete_user["access_token"]

        response = api_helpers.create_order(token, test_ingredients)
        response_data = response.json()

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is True
        assert response_data["name"]
        assert response_data["order"]["number"] is not None

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user, api_helpers):
        token = create_and_delete_user["access_token"]

        response = api_helpers.create_order(token, [])
        response_data = response.json()

        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}. Ответ: {response.text}"
        assert response_data["success"] is False
        assert response_data["message"] == TestData.ERROR_MESSAGES["no_ingredients"]

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient(self, create_and_delete_user, api_helpers):
        token = create_and_delete_user["access_token"]

        response = api_helpers.create_order(token, [TestData.INVALID_INGREDIENT])

        assert response.status_code == 500, f"Ожидался 500, получен {response.status_code}. Ответ: {response.text}"