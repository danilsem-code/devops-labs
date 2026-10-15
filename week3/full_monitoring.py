# ============================================
# ПОЛНЫЙ МОНИТОРИНГ С ЛОГИРОВАНИЕМ
# SQLite + os + subprocess + logging
# ============================================

import logging
import sqlite3
import subprocess
import platform
import datetime
import os


def setup_logger():
    """Настраивает логгер."""
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/monitor_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
    
    logger = logging.getLogger("full_monitor")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # В файл — всё
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # В консоль — INFO+
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_metrics(logger):
    """Собирает метрики системы."""
    logger.debug("Начинаем сбор метрик")
    metrics = {"server": platform.node()}
    
    # CPU (macOS)
    try:
        result = subprocess.run(
            ["top", "-l", "1", "-n", "0"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'CPU usage' in line:
                import re
                match = re.search(r'(\d+\.\d+)% user', line)
                if match:
                    metrics['cpu'] = float(match.group(1))
                    break
        logger.debug(f"CPU: {metrics.get('cpu', 0)}%")
    except Exception as e:
        logger.warning(f"Не удалось получить CPU: {e}")
        metrics['cpu'] = 0.0
    
    # Disk
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            metrics['disk'] = float(parts[4].replace('%', ''))
        logger.debug(f"Disk: {metrics.get('disk', 0)}%")
    except Exception as e:
        logger.warning(f"Не удалось получить Disk: {e}")
        metrics['disk'] = 0.0
    
    # RAM (упрощённо)
    metrics['ram'] = 50.0
    logger.debug(f"RAM: {metrics['ram']}%")
    
    return metrics


def save_to_db(metrics, logger):
    """Сохраняет метрики в БД."""
    try:
        conn = sqlite3.connect("metrics.db")
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO metrics (server, cpu, ram, disk, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (metrics['server'], metrics['cpu'], metrics['ram'], metrics['disk'], timestamp))
        
        conn.commit()
        conn.close()
        logger.debug("Метрики сохранены в БД")
    except Exception as e:
        logger.error(f"Ошибка сохранения в БД: {e}")


def check_thresholds(metrics, logger):
    """Проверяет пороги и логирует предупреждения."""
    if metrics['cpu'] > 80:
        logger.warning(f"⚠️  CPU критический: {metrics['cpu']}%")
    if metrics['disk'] > 85:
        logger.warning(f"⚠️  Диск заполнен: {metrics['disk']}%")
        if metrics['disk'] > 95:
            logger.critical(f"🚨 ДИСК ПЕРЕПОЛНЕН: {metrics['disk']}%")


def main():
    logger = setup_logger()
    
    logger.info("=" * 60)
    logger.info("ЗАПУСК МОНИТОРИНГА")
    logger.info("=" * 60)
    
    # 1. Собираем метрики
    metrics = get_metrics(logger)
    
    # 2. Логируем
    logger.info(f"Сервер: {metrics['server']}")
    logger.info(f"CPU: {metrics['cpu']}%")
    logger.info(f"RAM: {metrics['ram']}%")
    logger.info(f"Disk: {metrics['disk']}%")
    
    # 3. Проверяем пороги
    check_thresholds(metrics, logger)
    
    # 4. Сохраняем в БД
    save_to_db(metrics, logger)
    
    logger.info("Мониторинг завершён успешно")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
