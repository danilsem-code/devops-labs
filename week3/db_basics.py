# ============================================
# ОСНОВЫ SQLITE
# Создаём базу данных для метрик
# ============================================

import sqlite3
import datetime


def create_database():
    """Создаёт базу данных и таблицу."""
    # Подключаемся к базе (если файла нет — он создастся)
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    # Создаём таблицу
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            server TEXT NOT NULL,
            cpu REAL,
            ram REAL,
            disk REAL,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ База данных metrics.db создана!")


def add_metric(server, cpu, ram, disk):
    """Добавляет метрику в базу."""
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO metrics (server, cpu, ram, disk, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (server, cpu, ram, disk, timestamp))
    
    conn.commit()
    conn.close()
    print(f"✅ Добавлена метрика: {server} | CPU: {cpu}% | RAM: {ram}% | Disk: {disk}%")


def show_all_metrics():
    """Показывает все метрики."""
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM metrics ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print("📊 ВСЕ МЕТРИКИ")
    print("=" * 70)
    print(f"{'ID':<5} {'Сервер':<12} {'CPU':<8} {'RAM':<8} {'Disk':<8} {'Время'}")
    print("-" * 70)
    
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<12} {row[2]:<8} {row[3]:<8} {row[4]:<8} {row[5]}")
    
    print("=" * 70)
    print(f"Всего записей: {len(rows)}")
    
    conn.close()
def find_critical_servers(threshold=80):
    """Находит серверы с критической нагрузкой."""
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT server, cpu, ram, disk, timestamp
        FROM metrics
        WHERE cpu > ? OR ram > ? OR disk > ?
        ORDER BY timestamp DESC
    """, (threshold, threshold, threshold))
    
    rows = cursor.fetchall()
    
    print(f"\n⚠️  СЕРВЕРЫ С НАГРУЗКОЙ > {threshold}%:")
    print("-" * 70)
    
    if rows:
        for row in rows:
            print(f"🔴 {row[0]:<12} | CPU: {row[1]}% | RAM: {row[2]}% | Disk: {row[3]}% | {row[4]}")
    else:
        print("✅ Нет серверов с критической нагрузкой")
    
    conn.close()


def get_server_stats(server_name):
    """Показывает статистику по серверу."""
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as count,
            AVG(cpu) as avg_cpu,
            MAX(cpu) as max_cpu,
            AVG(ram) as avg_ram,
            MAX(ram) as max_ram
        FROM metrics
        WHERE server = ?
    """, (server_name,))
    
    row = cursor.fetchone()
    
    print(f"\n📊 Статистика по {server_name}:")
    print(f"   Замеров: {row[0]}")
    print(f"   CPU: среднее {row[1]:.1f}%, максимум {row[2]:.1f}%")
    print(f"   RAM: среднее {row[3]:.1f}%, максимум {row[4]:.1f}%")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 70)
    print("SQLITE: БАЗА ДАННЫХ МЕТРИК")
    print("=" * 70)
    
    # 1. Создаём базу
    create_database()
    
    # 2. Добавляем тестовые метрики
    print("\n--- Добавление метрик ---")
    add_metric("web-01", 45.2, 60.1, 70.5)
    add_metric("db-01", 80.5, 90.2, 50.0)
    add_metric("backup-01", 15.3, 30.5, 95.0)
    add_metric("web-02", 55.0, 65.0, 60.0)
    
    # 3. Показываем всё
    show_all_metrics()
    # 4. Ищем критичные серверы
    find_critical_servers(threshold=80)
    
    # 5. Статистика по серверу
    get_server_stats("web-01")
