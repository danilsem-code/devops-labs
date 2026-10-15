# ============================================
# ЗАПУСК СИСТЕМНЫХ КОМАНД (subprocess)
# DevOps: автоматизация системных операций
# ============================================

import subprocess
import platform


def run_command(cmd):
    """Запускает команду и возвращает результат."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=True  # Для простоты (но менее безопасно)
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"❌ Ошибка: {result.stderr.strip()}"
    
    except subprocess.TimeoutExpired:
        return "⏰ Таймаут"
    except Exception as e:
        return f"❌ Исключение: {e}"


def check_ping(host):
    """Проверяет доступность хоста через ping."""
    if platform.system() == "Windows":
        cmd = f"ping -n 1 {host}"
    else:
        cmd = f"ping -c 1 {host}"
    
    result = run_command(cmd)
    
    if "ttl" in result.lower() or "time=" in result.lower():
        return f"✅ {host} доступен"
    else:
        return f"❌ {host} недоступен"


def get_system_info():
    """Собирает информацию о системе."""
    commands = {
        "Имя хоста": "hostname",
        "Пользователь": "whoami",
        "Диск": "df -h /",
        "Процессы Python": "ps aux | grep python | head -3",
    }
    
    print("=" * 70)
    print("СИСТЕМНАЯ ИНФОРМАЦИЯ (через subprocess)")
    print("=" * 70)
    
    for name, cmd in commands.items():
        print(f"\n📌 {name}:")
        print("-" * 50)
        result = run_command(cmd)
        print(result)


def run_ping_scan(hosts):
    """Проверяет список хостов через ping."""
    print("\n" + "=" * 70)
    print("PING-СКАН ХОСТОВ")
    print("=" * 70)
    
    for host in hosts:
        print(f"  {check_ping(host)}")


if __name__ == "__main__":
    # 1. Информация о системе
    get_system_info()
    
    # 2. Ping-скан
    hosts = ["8.8.8.8", "1.1.1.1", "google.com", "192.168.1.1"]
    run_ping_scan(hosts)
    
    print("\n" + "=" * 70)
    print("✅ Готово!")
    print("=" * 70)
