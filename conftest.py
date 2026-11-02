import time
import random

import pytest
from faker import Faker

from data.config import BASE_URL
from data.test_data import TestData
from helpers.api_helpers import ApiHelpers

fake = Faker()


@pytest.fixture(scope="function")
def api_helpers():
    """Хелпер для работы с API"""
    return ApiHelpers(BASE_URL)


@pytest.fixture(scope="function")
def create_and_delete_user(api_helpers):
    """Создаёт уникального пользователя до теста и удаляет после"""
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)

    user_data = {
        "email": f"test_user_{timestamp}_{random_suffix}@test.com",
        "password": f"Pass{timestamp}{random_suffix}!",
        "name": f"TestUser_{timestamp}_{random_suffix}",
    }

    response = api_helpers.create_user(user_data)
    assert response is not None, "Сервер не отвечает"
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    response_data = response.json()
    full_token = response_data["accessToken"]
    access_token = full_token.replace("Bearer ", "") if full_token.startswith("Bearer ") else full_token

    yield {
        "data": user_data,
        "access_token": access_token,
        "full_token": full_token,
        "refresh_token": response_data.get("refreshToken"),
    }

    api_helpers.delete_user(full_token)


@pytest.fixture(scope="function")
def cleanup_created_users(api_helpers):
    """Для тестов регистрации: собирает токены, удаляет пользователей после теста"""
    tokens = []
    yield tokens
    for token in tokens:
        api_helpers.delete_user(token)


@pytest.fixture(scope="function")
def test_ingredients(api_helpers):
    """Возвращает список ID ингредиентов (или fallback, если API недоступен)"""
    response = api_helpers.get_ingredients()
    if response is None or response.status_code != 200:
        return TestData.VALID_INGREDIENTS

    response_data = response.json()
    if not response_data.get("data"):
        return TestData.VALID_INGREDIENTS

    return [ing["_id"] for ing in response_data["data"]][:3]