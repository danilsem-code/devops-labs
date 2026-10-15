# ============================================
# ЧТЕНИЕ JSON-КОНФИГА
# DevOps практика: парсинг конфигов серверов
# ============================================

import json


def load_config(filename):
    """Загружает JSON-конфиг из файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден!")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка в JSON: {e}")
        return None


def print_servers(config):
    """Выводит список серверов из конфига."""
    print("=" * 60)
    print(f"🌍 Окружение: {config['environment']}")
    print("=" * 60)
    
    servers = config['servers']
    print(f"\n📊 Всего серверов: {len(servers)}\n")
    
    for server in servers:
        status = "✅" if server['enabled'] else "❌"
        print(f"{status} {server['name']:12} | {server['ip']:15} | "
              f"порт: {server['port']:5} | роль: {server['role']}")
    
    # Статистика
    enabled = sum(1 for s in servers if s['enabled'])
    disabled = len(servers) - enabled
    print(f"\n📈 Активных: {enabled} | Отключённых: {disabled}")


def print_monitoring(config):
    """Выводит настройки мониторинга."""
    mon = config['monitoring']
    print("\n" + "=" * 60)
    print("📡 Мониторинг:")
    print(f"   Интервал: {mon['interval_seconds']} сек")
    print(f"   Email для алертов: {mon['alert_email']}")
    print("=" * 60)


# ============================================
# ОСНОВНАЯ ЧАСТЬ
# ============================================

if __name__ == "__main__":
    print("🔍 Загрузка конфига servers.json...\n")
    
    config = load_config("servers.json")
    
    if config:
        print_servers(config)
        print_monitoring(config)
        print("\n✅ Конфиг успешно обработан!")
