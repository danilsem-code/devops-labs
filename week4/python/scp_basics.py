# ============================================
# ОСНОВЫ SCP (SFTP через paramiko)
# Копируем файлы между машинами
# ============================================

import paramiko
import os


def connect_sftp(host, username, password=None):
    """Подключается к серверу и открывает SFTP-сессию."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=10)
        sftp = client.open_sftp()
        print(f"✅ SFTP подключен к {host}")
        return client, sftp
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None, None


def upload_file(sftp, local_path, remote_path):
    """Загружает файл на сервер."""
    try:
        if not os.path.exists(local_path):
            print(f"❌ Локальный файл не найден: {local_path}")
            return False
        
        sftp.put(local_path, remote_path)
        print(f"✅ Загружено: {local_path} → {remote_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return False


def download_file(sftp, remote_path, local_path):
    """Скачивает файл с сервера."""
    try:
        sftp.get(remote_path, local_path)
        print(f"✅ Скачано: {remote_path} → {local_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False


def list_remote_files(sftp, remote_path="."):
    """Показывает файлы на удалённом сервере."""
    try:
        files = sftp.listdir(remote_path)
        print(f"\n📁 Содержимое {remote_path}:")
        for f in files:
            print(f"   - {f}")
        return files
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []


if __name__ == "__main__":
    HOST = "localhost"
    USERNAME = "danilsemenov"
    PASSWORD = "lfybkctvtyjd"  # ⚠️ Замени на пароль, если ключ не работает
    
    print("=" * 60)
    print("SCP (SFTP) — БАЗОВЫЙ ПРИМЕР")
    print("=" * 60)
    
    # 1. Подключаемся
    client, sftp = connect_sftp(HOST, USERNAME, PASSWORD)
    
    if not client:
        exit(1)
    
    # 2. Создаём локальный файл для теста
    with open("test_upload.txt", "w") as f:
        f.write("Привет с сервера!\n")
        f.write("Это тестовый файл для SCP.\n")
    
    print("\n📝 Создан локальный файл test_upload.txt")
    
    # 3. Загружаем на "удалённый" сервер (localhost)
    remote_path = "/tmp/test_upload.txt"
    upload_file(sftp, "test_upload.txt", remote_path)
    
    # 4. Проверяем, что файл на месте
    list_remote_files(sftp, "/tmp")
    
    # 5. Скачиваем обратно
    download_file(sftp, remote_path, "test_download.txt")
    
    # 6. Проверяем содержимое
    print("\n📄 Содержимое скачанного файла:")
    with open("test_download.txt") as f:
        print(f.read())
    
    # 7. Закрываем
    sftp.close()
    client.close()
    print("\n" + "=" * 60)
    print("✅ Соединение закрыто")
