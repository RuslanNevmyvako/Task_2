import pytest
import allure
from faker import Faker
from helpers.api_helpers import ApiHelpers

fake = Faker()
BASE_URL = "https://stellarburgers.education-services.ru/api"


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    """Тесты для изменения данных пользователя"""
    
    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("field_to_update", ["email", "name"])
    def test_update_user_with_auth(self, create_and_delete_user, api_helpers, field_to_update):
        """Тест изменения данных пользователя с авторизацией"""
        
        assert create_and_delete_user is not None, "Пользователь не создан"
        
        user_data = create_and_delete_user["data"]
        token = create_and_delete_user["access_token"]
        
        # Проверяем, что токен есть
        assert token is not None, "Токен не получен"
        assert len(token) > 0, "Токен пустой"
        
        # Подготавливаем данные для обновления
        update_data = {}
        if field_to_update == "email":
            # Используем unique для гарантии уникальности
            update_data["email"] = fake.unique.email()
        else:
            update_data["name"] = fake.unique.name()
        
        print(f"🟢 Обновляем {field_to_update} на: {update_data[field_to_update]}")
        
        response = api_helpers.update_user(token, update_data)
        
        # Проверяем, что ответ получен
        assert response is not None, "Ответ от сервера не получен (None)"
        
        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is True
        
        if field_to_update == "email":
            assert response_data["user"]["email"] == update_data["email"]
        else:
            assert response_data["user"]["name"] == update_data["name"]
        
        print(f"✅ {field_to_update} успешно обновлен")
    
    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth(self, api_helpers):
        """Тест изменения данных пользователя без авторизации"""
        update_data = {
            "email": fake.unique.email(),
            "name": fake.unique.name()
        }
        
        print(f"🟢 Обновление без авторизации: {update_data}")
        
        # Отправляем запрос без токена
        response = api_helpers.update_user("", update_data)
        
        # Проверяем, что ответ получен
        assert response is not None, "Ответ от сервера не получен (None)"
        
        # Проверяем код ответа
        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data["success"] is False
        assert "You should be authorised" in response_data["message"]
        
        print("✅ Запрос без авторизации вернул 401")