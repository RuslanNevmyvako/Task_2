import requests
import time


class ApiHelpers:
    """Хелпер для работы с API Stellar Burgers"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.max_retries = 3
        self.retry_delay = 2
    
    def _make_request(self, method, url, **kwargs):
        """
        Универсальный метод с повторными попытками.
        ВОЗВРАЩАЕТ ЛЮБОЙ ОТВЕТ (даже 500), а не только успешный.
        """
        last_response = None
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                print(f"📡 Попытка {attempt + 1}/{self.max_retries}: {method} {url}")
                response = requests.request(method, url, timeout=10, **kwargs)
                
                # ВСЕГДА возвращаем ответ, даже если это 500
                # Не делаем повторных попыток на 500, потому что это может быть ожидаемым результатом
                return response
                
            except requests.exceptions.Timeout:
                print(f"⏰ Таймаут при попытке {attempt + 1}")
                last_error = "Timeout"
                time.sleep(self.retry_delay)
                
            except requests.exceptions.ConnectionError:
                print(f"🔌 Ошибка соединения при попытке {attempt + 1}")
                last_error = "ConnectionError"
                time.sleep(self.retry_delay)
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                last_error = str(e)
                time.sleep(self.retry_delay)
        
        # Если все попытки провалились из-за ошибок соединения
        print(f"❌ Не удалось выполнить запрос после {self.max_retries} попыток")
        return None
    
    def create_user(self, user_data):
        """Создание пользователя"""
        url = f"{self.base_url}/auth/register"
        return self._make_request('POST', url, json=user_data)
    
    def login_user(self, login_data):
        """Авторизация пользователя"""
        url = f"{self.base_url}/auth/login"
        return self._make_request('POST', url, json=login_data)
    
    def update_user(self, token, user_data):
        """Обновление данных пользователя"""
        url = f"{self.base_url}/auth/user"
        
        headers = {}
        if token:
            if not token.startswith("Bearer "):
                headers["Authorization"] = f"Bearer {token}"
            else:
                headers["Authorization"] = token
        
        return self._make_request('PATCH', url, json=user_data, headers=headers)
    
    def get_user(self, token):
        """Получение данных пользователя"""
        url = f"{self.base_url}/auth/user"
        if token:
            if not token.startswith("Bearer "):
                headers = {"Authorization": f"Bearer {token}"}
            else:
                headers = {"Authorization": token}
        else:
            headers = {}
        return self._make_request('GET', url, headers=headers)
    
    def create_order(self, token, ingredients):
        """Создание заказа"""
        url = f"{self.base_url}/orders"
        headers = {}
        if token:
            if not token.startswith("Bearer "):
                headers["Authorization"] = f"Bearer {token}"
            else:
                headers["Authorization"] = token
        data = {"ingredients": ingredients}
        return self._make_request('POST', url, json=data, headers=headers)
    
    def get_orders(self, token):
        """Получение заказов пользователя"""
        url = f"{self.base_url}/orders"
        if token:
            if not token.startswith("Bearer "):
                headers = {"Authorization": f"Bearer {token}"}
            else:
                headers = {"Authorization": token}
        else:
            headers = {}
        return self._make_request('GET', url, headers=headers)
    
    def get_ingredients(self):
        """Получение списка ингредиентов"""
        url = f"{self.base_url}/ingredients"
        return self._make_request('GET', url)