# ============================================
# ЛОГИРОВАНИЕ В ФАЙЛ
# DevOps: сохраняем логи для анализа
# ============================================

import logging
import os
from datetime import datetime


def setup_logger(name, log_file):
    """Настраивает логгер с записью в файл."""
    # Создаём папку для логов, если нет
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Формат
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # В консоль только INFO+
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def simulate_monitoring(logger):
    """Имитирует мониторинг серверов."""
    logger.info("Запуск мониторинга")
    
    servers = [
        {"name": "web-01", "status": "ok", "cpu": 45},
        {"name": "db-01", "status": "ok", "cpu": 80},
        {"name": "backup-01", "status": "error", "cpu": 0},
    ]
    
    for server in servers:
        if server["status"] == "ok":
            logger.info(f"✅ {server['name']}: работает (CPU: {server['cpu']}%)")
            
            if server["cpu"] > 75:
                logger.warning(f"⚠️  {server['name']}: высокая нагрузка CPU ({server['cpu']}%)")
        else:
            logger.error(f"❌ {server['name']}: недоступен!")
            logger.critical(f"🚨 {server['name']}: требует немедленного вмешательства!")
    
    logger.info("Мониторинг завершён")


if __name__ == "__main__":
    # Настраиваем логгер
    log_file = f"logs/monitoring_{datetime.now().strftime('%Y-%m-%d')}.log"
    logger = setup_logger("monitoring", log_file)
    
    # Запускаем мониторинг
    simulate_monitoring(logger)
    
    print(f"\n📄 Логи сохранены в: {log_file}")
