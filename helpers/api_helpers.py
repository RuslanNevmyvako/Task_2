import time
import allure
import requests

from data.config import (
    ENDPOINT_REGISTER,
    ENDPOINT_LOGIN,
    ENDPOINT_USER,
    ENDPOINT_ORDERS,
    ENDPOINT_INGREDIENTS,
)


class ApiHelpers:
    """Хелпер для работы с API Stellar Burgers"""

    def __init__(self, base_url):
        self.base_url = base_url
        self.max_retries = 3
        self.retry_delay = 2

    def _make_request(self, method, url, **kwargs):
        """Универсальный метод с повторными попытками"""
        for attempt in range(self.max_retries):
            try:
                return requests.request(method, url, timeout=10, **kwargs)
            except Exception:
                time.sleep(self.retry_delay)
        return None

    @allure.step("Создание пользователя")
    def create_user(self, user_data):
        url = f"{self.base_url}{ENDPOINT_REGISTER}"
        return self._make_request('POST', url, json=user_data)

    @allure.step("Авторизация пользователя")
    def login_user(self, login_data):
        url = f"{self.base_url}{ENDPOINT_LOGIN}"
        return self._make_request('POST', url, json=login_data)

    @allure.step("Обновление данных пользователя")
    def update_user(self, token, user_data):
        url = f"{self.base_url}{ENDPOINT_USER}"
        headers = self._build_auth_headers(token)
        return self._make_request('PATCH', url, json=user_data, headers=headers)

    @allure.step("Получение данных пользователя")
    def get_user(self, token):
        url = f"{self.base_url}{ENDPOINT_USER}"
        headers = self._build_auth_headers(token)
        return self._make_request('GET', url, headers=headers)

    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        url = f"{self.base_url}{ENDPOINT_USER}"
        headers = self._build_auth_headers(token)
        return self._make_request('DELETE', url, headers=headers)

    @allure.step("Создание заказа")
    def create_order(self, token, ingredients):
        url = f"{self.base_url}{ENDPOINT_ORDERS}"
        headers = self._build_auth_headers(token)
        data = {"ingredients": ingredients}
        return self._make_request('POST', url, json=data, headers=headers)

    @allure.step("Получение заказов пользователя")
    def get_orders(self, token):
        url = f"{self.base_url}{ENDPOINT_ORDERS}"
        headers = self._build_auth_headers(token)
        return self._make_request('GET', url, headers=headers)

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        url = f"{self.base_url}{ENDPOINT_INGREDIENTS}"
        return self._make_request('GET', url)

    @staticmethod
    def _build_auth_headers(token):
        """Формирует заголовок Authorization из токена"""
        if not token:
            return {}
        if not token.startswith("Bearer "):
            return {"Authorization": f"Bearer {token}"}
        return {"Authorization": token}