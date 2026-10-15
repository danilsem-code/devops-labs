# ============================================
# ОСНОВЫ ЛОГИРОВАНИЯ
# Первый лог в Python
# ============================================

import logging

# Настраиваем логирование
logging.basicConfig(
    level=logging.DEBUG,  # Минимальный уровень для вывода
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Создаём логгер
logger = logging.getLogger(__name__)


def main():
    logger.debug("Это отладочное сообщение (DEBUG)")
    logger.info("Программа запущена (INFO)")
    logger.warning("Что-то подозрительное (WARNING)")
    logger.error("Произошла ошибка (ERROR)")
    logger.critical("Критическая ошибка! (CRITICAL)")


if __name__ == "__main__":
    main()
