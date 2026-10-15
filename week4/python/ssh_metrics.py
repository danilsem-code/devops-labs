# ============================================
# СБОР МЕТРИК С УДАЛЁННОГО СЕРВЕРА
# DevOps: мониторинг инфраструктуры
# ============================================

import paramiko


def get_remote_metrics(host, username, password=None):
    """
    Подключается к серверу и собирает метрики.
    Возвращает словарь с метриками.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    metrics = {"host": host}
    
    try:
        # Подключаемся
        client.connect(host, username=username, password=password, timeout=10)
        
        # 1. Hostname
        _, stdout, _ = client.exec_command("hostname")
        metrics["hostname"] = stdout.read().decode().strip()
        
        # 2. Uptime
        _, stdout, _ = client.exec_command("uptime")
        metrics["uptime"] = stdout.read().decode().strip()
        
        # 3. Диск
        _, stdout, _ = client.exec_command("df -h / | tail -1")
        disk_line = stdout.read().decode().strip()
        if disk_line:
            parts = disk_line.split()
            metrics["disk_total"] = parts[1]
            metrics["disk_used"] = parts[2]
            metrics["disk_free"] = parts[3]
            metrics["disk_percent"] = parts[4]
        
        # 4. Процессы
        _, stdout, _ = client.exec_command("ps aux | wc -l")
        metrics["processes"] = stdout.read().decode().strip()
        
        client.close()
        metrics["status"] = "ok"
    
    except Exception as e:
        metrics["status"] = "error"
        metrics["error"] = str(e)
    
    return metrics


def print_metrics(metrics):
    """Красиво выводит метрики."""
    print("=" * 60)
    print(f"📊 МЕТРИКИ СЕРВЕРА: {metrics['host']}")
    print("=" * 60)
    
    if metrics["status"] != "ok":
        print(f"❌ Ошибка: {metrics.get('error', 'неизвестно')}")
        return
    
    print(f"🖥️  Hostname:  {metrics.get('hostname', 'N/A')}")
    print(f"⏱️  Uptime:    {metrics.get('uptime', 'N/A')}")
    print(f"💾 Диск:")
    print(f"   Всего:     {metrics.get('disk_total', 'N/A')}")
    print(f"   Занято:    {metrics.get('disk_used', 'N/A')}")
    print(f"   Свободно:  {metrics.get('disk_free', 'N/A')}")
    print(f"   Процент:   {metrics.get('disk_percent', 'N/A')}")
    print(f"🧠 Процессы:  {metrics.get('processes', 'N/A')}")
    print("=" * 60)


if __name__ == "__main__":
    # === НАСТРОЙКИ ===
    HOST = "localhost"
    USERNAME = "danilsemenov"
    
    # ⚠️ ВАЖНО: выбери одно из двух!
    
    # Вариант 1: SSH-ключ (если настроен)
    PASSWORD = None
    
    # Вариант 2: Пароль (замени на свой и раскомментируй)
    # PASSWORD = "твой_пароль_от_мака"
    
    metrics = get_remote_metrics(
        host=HOST,
        username=USERNAME,
        password=""
    )
    
    print_metrics(metrics)
