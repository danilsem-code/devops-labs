# ============================================
# МОНИТОРИНГ СИСТЕМЫ С ЗАПИСЬЮ В БД
# Реальный DevOps-инструмент
# ============================================

import sqlite3
import subprocess
import datetime
import platform
import re


def get_system_metrics():
    """Получает текущие метрики системы (macOS/Linux)."""
    metrics = {}
    
    # CPU (упрощённо — нагрузка)
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ["top", "-l", "1", "-n", "0"],
                capture_output=True, text=True, timeout=5
            )
            # Извлекаем CPU usage
            for line in result.stdout.split('\n'):
                if 'CPU usage' in line:
                    match = re.search(r'(\d+\.\d+)% user', line)
                    if match:
                        metrics['cpu'] = float(match.group(1))
                        break
        else:  # Linux
            with open('/proc/loadavg', 'r') as f:
                load = float(f.read().split()[0])
                metrics['cpu'] = min(load * 100, 100)
    except Exception as e:
        print(f"⚠️  Не удалось получить CPU: {e}")
        metrics['cpu'] = 0.0
    
    # RAM
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(
                ["vm_stat"], capture_output=True, text=True, timeout=5
            )
            # Упрощённо: считаем свободную память
            metrics['ram'] = 50.0  # заглушка для macOS
        else:
            with open('/proc/meminfo', 'r') as f:
                mem = f.read()
                total = int(re.search(r'MemTotal:\s+(\d+)', mem).group(1))
                available = int(re.search(r'MemAvailable:\s+(\d+)', mem).group(1))
                metrics['ram'] = round((1 - available/total) * 100, 1)
    except Exception as e:
        print(f"⚠️  Не удалось получить RAM: {e}")
        metrics['ram'] = 0.0
    
    # Disk
    try:
        result = subprocess.run(
            ["df", "-h", "/"], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            disk_str = parts[4].replace('%', '')
            metrics['disk'] = float(disk_str)
    except Exception as e:
        print(f"⚠️  Не удалось получить Disk: {e}")
        metrics['disk'] = 0.0
    
    return metrics


def save_to_db(server_name, metrics):
    """Сохраняет метрики в БД."""
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO metrics (server, cpu, ram, disk, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (server_name, metrics['cpu'], metrics['ram'], metrics['disk'], timestamp))
    
    conn.commit()
    conn.close()


def main():
    server_name = platform.node()  # Имя твоего Mac
    
    print("=" * 70)
    print(f"📊 МОНИТОРИНГ: {server_name}")
    print("=" * 70)
    
    # Получаем метрики
    metrics = get_system_metrics()
    
    print(f"CPU:  {metrics['cpu']}%")
    print(f"RAM:  {metrics['ram']}%")
    print(f"Disk: {metrics['disk']}%")
    
    # Сохраняем в БД
    save_to_db(server_name, metrics)
    print(f"\n✅ Метрики сохранены в базу данных")
    
    # Показываем последние 5 записей
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    
    print("\n📋 Последние 5 записей:")
    print("-" * 70)
    for row in rows:
        print(f"ID: {row[0]} | {row[1]} | CPU: {row[2]}% | RAM: {row[3]}% | Disk: {row[4]}% | {row[5]}")
    
    conn.close()


if __name__ == "__main__":
    main()
