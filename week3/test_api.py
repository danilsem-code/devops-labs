# ============================================
# ПЕРВЫЙ REST API ЗАПРОС
# Получаем данные с публичного API
# ============================================

import requests
import json


def get_github_user(username):
    """Получает информацию о пользователе GitHub через API."""
    url = f"https://api.github.com/users/{username}"
    
    print(f"🌐 Запрос к: {url}")
    response = requests.get(url)
    
    print(f"📊 Статус: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Пользователь найден!")
        print(f"   Имя: {data.get('name', 'не указано')}")
        print(f"   Логин: {data['login']}")
        print(f"   Публичных репозиториев: {data['public_repos']}")
        print(f"   Подписчиков: {data['followers']}")
        print(f"   Создан: {data['created_at']}")
    else:
        print(f"❌ Ошибка: {response.status_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТ GITHUB API")
    print("=" * 60)
    
    # Запрос к своему профилю
    get_github_user("danilsem-code")
