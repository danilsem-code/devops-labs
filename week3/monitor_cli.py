# ============================================
# CLI-ИНСТРУМЕНТ ДЛЯ МОНИТОРИНГА
# DevOps-инструмент с аргументами
# ============================================

import argparse
import subprocess
import platform
import sys
import logging
from datetime import datetime


def setup_logger(verbose=False):
    """Настраивает логгер."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    return logging.getLogger(__name__)


def ping_host(host, timeout=2):
    """Проверяет доступность хоста."""
    param = '-n' if platform.system() == 'Windows' else '-c'
    try:
        result = subprocess.run(
            ['ping', param, '1', '-W', str(timeout), host],
            capture_output=True,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except:
        return False


def cmd_check(args, logger):
    """Команда: проверка хостов."""
    logger.info(f"Проверка {len(args.hosts)} хостов...")
    
    results = []
    for host in args.hosts:
        logger.debug(f"Ping {host}...")
        is_up = ping_host(host, args.timeout)
        
        if is_up:
            logger.info(f"✅ {host} — доступен")
        else:
            logger.error(f"❌ {host} — недоступен")
        
        results.append((host, is_up))
    
    # Итог
    up = sum(1 for _, status in results if status)
    down = len(results) - up
    
    logger.info(f"\nИтог: ✅ {up} доступно | ❌ {down} недоступно")
    
    if down > 0 and args.exit_on_fail:
        sys.exit(1)


def cmd_info(args, logger):
    """Команда: информация о системе."""
    logger.info("Сбор информации о системе...")
    
    print(f"\n{'=' * 50}")
    print(f"ИНФОРМАЦИЯ О СИСТЕМЕ")
    print(f"{'=' * 50}")
    print(f"Хост:      {platform.node()}")
    print(f"Система:   {platform.system()} {platform.release()}")
    print(f"Python:    {sys.version.split()[0]}")
    print(f"Время:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}")


def main():
    # Главный парсер
    parser = argparse.ArgumentParser(
        description="DevOps Monitor CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 monitor_cli.py check 8.8.8.8 1.1.1.1
  python3 monitor_cli.py check 8.8.8.8 --timeout 5 --verbose
  python3 monitor_cli.py info
  python3 monitor_cli.py check google.com --exit-on-fail
        """
    )
    
    # Глобальные аргументы
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Подробный вывод (DEBUG)"
    )
    
    # Подкоманды
    subparsers = parser.add_subparsers(dest="command", help="Команды")
    
    # Команда: check
    check_parser = subparsers.add_parser("check", help="Проверить хосты")
    check_parser.add_argument(
        "hosts",
        nargs="+",  # Один или больше
        help="Хосты для проверки (IP или домены)"
    )
    check_parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=2,
        help="Таймаут в секундах (по умолчанию: 2)"
    )
    check_parser.add_argument(
        "--exit-on-fail",
        action="store_true",
        help="Выход с кодом 1, если есть недоступные"
    )
    
    # Команда: info
    info_parser = subparsers.add_parser("info", help="Информация о системе")
    
    # Парсим
    args = parser.parse_args()
    
    # Если команда не указана — показать помощь
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Настраиваем логгер
    logger = setup_logger(args.verbose)
    
    # Выполняем команду
    if args.command == "check":
        cmd_check(args, logger)
    elif args.command == "info":
        cmd_info(args, logger)


if __name__ == "__main__":
    main()
