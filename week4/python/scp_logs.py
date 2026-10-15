# ============================================
# СКАЧИВАНИЕ ЛОГОВ С СЕРВЕРА
# DevOps: сбор логов для анализа
# ============================================

import paramiko
import os
import datetime


def download_logs(host, username, password=None, remote_dir="/var/log", local_dir="logs_from_server"):
    """Скачивает логи с сервера."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=10)
        sftp = client.open_sftp()
        
        # Создаём локальную папку
        os.makedirs(local_dir, exist_ok=True)
        
        # Получаем список файлов
        try:
            files = sftp.listdir(remote_dir)
        except PermissionError:
            print(f"⚠️  Нет доступа к {remote_dir}, используем ~/devops-labs")
            remote_dir = f"/Users/{username}/devops-labs"
            files = sftp.listdir(remote_dir)
        
        downloaded = 0
        
        for filename in files:
            remote_path = f"{remote_dir}/{filename}"
            
            # Пропускаем папки
            try:
                sftp.stat(remote_path)
            except:
                continue
            
            # Пропускаем большие файлы (>1MB)
            try:
                size = sftp.stat(remote_path).st_size
                if size > 1024 * 1024:
                    print(f"⏭️  Пропускаем (большой): {filename} ({size // 1024} KB)")
                    continue
            except:
                continue
            
            local_path = f"{local_dir}/{filename}"
            
            try:
                sftp.get(remote_path, local_path)
                print(f"✅ Скачано: {filename}")
                downloaded += 1
            except Exception as e:
                print(f"❌ {filename}: {e}")
        
        sftp.close()
        client.close()
        
        print(f"\n📊 Итого скачано: {downloaded} файлов")
        print(f"📁 Папка: {local_dir}/")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    HOST = "localhost"
    USERNAME = "danilsemenov"
    PASSWORD = "lfybkctvtyjd"  # ⚠️ Замени, если ключ не работает
    
    print("=" * 60)
    print("СКАЧИВАНИЕ ЛОГОВ С СЕРВЕРА")
    print("=" * 60)
    
    download_logs(
        host=HOST,
        username=USERNAME,
        password=PASSWORD,
        remote_dir=f"/Users/{USERNAME}/devops-labs/week4/logs",
        local_dir="logs_from_server"
    )
