"""Тестовые данные для API тестов"""


class TestData:
    """Класс с тестовыми данными"""
    
    # Валидные ингредиенты (берем из документации)
    VALID_INGREDIENTS = [
        "60d3b41abdacab0026a733c6",  # bun
        "60d3b41abdacab0026a733c7",  # bun
        "609646e4dc916e00276b2870"   # sauce
    ]
    
    # Невалидный хеш ингредиента
    INVALID_INGREDIENT = "invalid_hash_123"
    
    # Сообщения об ошибках
    ERROR_MESSAGES = {
        "user_exists": "User already exists",
        "required_fields": "Email, password and name are required fields",
        "invalid_credentials": "email or password are incorrect",
        "no_ingredients": "Ingredient ids must be provided",
        "unauthorized": "You should be authorised"
    }