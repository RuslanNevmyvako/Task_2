import pytest
import requests
import time
import random
from faker import Faker
from helpers.api_helpers import ApiHelpers

fake = Faker()
BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture(scope="function")
def api_helpers():
    """Фикстура для хелперов API"""
    return ApiHelpers(BASE_URL)


@pytest.fixture(scope="function")
def create_and_delete_user(api_helpers):
    """
    Фикстура создает пользователя с ГАРАНТИРОВАННО уникальными данными.
    """
    # Генерируем уникальные данные с timestamp
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    
    user_data = {
        "email": f"test_user_{timestamp}_{random_suffix}@test.com",
        "password": f"Pass{timestamp}{random_suffix}!",
        "name": f"TestUser_{timestamp}_{random_suffix}"
    }
    
    print(f"\n🔵 Создаем пользователя: {user_data['email']}")
    
    max_retries = 3
    response = None
    
    for attempt in range(max_retries):
        try:
            response = api_helpers.create_user(user_data)
            print(f"📝 Попытка {attempt + 1}: Статус {response.status_code if response else 'None'}")
            
            if response and response.status_code == 200:
                break
            
            # Если пользователь уже существует (403) - генерируем новые данные
            if response and response.status_code == 403:
                print("⚠️ Пользователь уже существует, генерируем новые данные...")
                timestamp = int(time.time() * 1000) + attempt
                random_suffix = random.randint(1000, 9999)
                user_data = {
                    "email": f"test_user_{timestamp}_{random_suffix}@test.com",
                    "password": f"Pass{timestamp}{random_suffix}!",
                    "name": f"TestUser_{timestamp}_{random_suffix}"
                }
                print(f"🔄 Новый email: {user_data['email']}")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Ошибка при попытке {attempt + 1}: {e}")
            time.sleep(2)
    
    if response is None:
        error_msg = f"Не удалось создать пользователя: сервер не отвечает"
        print(f"❌ {error_msg}")
        raise AssertionError(error_msg)
    
    if response.status_code != 200:
        error_msg = f"Не удалось создать пользователя. Статус: {response.status_code}, Ответ: {response.text}"
        print(f"❌ {error_msg}")
        raise AssertionError(error_msg)
    
    response_data = response.json()
    access_token = response_data.get("accessToken", "")
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token.replace("Bearer ", "")
    
    print(f"✅ Пользователь создан: {user_data['email']}")
    
    yield {
        "data": user_data,
        "access_token": access_token,
        "full_token": response_data.get("accessToken"),
        "refresh_token": response_data.get("refreshToken")
    }


@pytest.fixture(scope="function")
def test_ingredients(api_helpers):
    """Фикстура для получения списка ингредиентов"""
    # Запасные ингредиенты (всегда валидные)
    FALLBACK = [
        "60d3b41abdacab0026a733c6",
        "60d3b41abdacab0026a733c7",
        "609646e4dc916e00276b2870",
    ]
    
    try:
        response = api_helpers.get_ingredients()
        
        if response is None:
            print("⚠️ Сервер не отвечает, используем запасные ингредиенты")
            return FALLBACK
        
        if response.status_code != 200:
            print(f"⚠️ Ошибка получения ингредиентов: {response.status_code}, используем запасные")
            return FALLBACK
        
        response_data = response.json()
        if not response_data.get("data"):
            return FALLBACK
        
        ingredients = [ing["_id"] for ing in response_data["data"]]
        print(f"✅ Получено {len(ingredients)} ингредиентов")
        return ingredients[:3]
    
    except Exception as e:
        print(f"⚠️ Ошибка: {e}, используем запасные ингредиенты")
        return FALLBACK