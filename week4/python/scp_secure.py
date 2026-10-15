# ============================================
# БЕЗОПАСНЫЙ SCP С .env
# Пароли хранятся в .env, не в коде!
# ============================================

import paramiko
import os
from dotenv import load_dotenv


# Загружаем .env
load_dotenv()


def connect_sftp(host, username, password):
    """Подключается к серверу и открывает SFTP."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=10)
        sftp = client.open_sftp()
        print(f"✅ SFTP подключен к {host} (пользователь: {username})")
        return client, sftp
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return None, None


def upload_file(sftp, local_path, remote_path):
    """Загружает файл на сервер."""
    try:
        sftp.put(local_path, remote_path)
        print(f"✅ Загружено: {local_path} → {remote_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("БЕЗОПАСНЫЙ SCP (секреты в .env)")
    print("=" * 60)
    
    # Читаем секреты из .env
    HOST = os.getenv("SSH_HOST", "localhost")
    USER = os.getenv("SSH_USER")
    PASSWORD = os.getenv("SSH_PASSWORD")
    
    # Проверяем, что всё загружено
    if not USER or not PASSWORD:
        print("❌ Не заданы SSH_USER или SSH_PASSWORD в .env")
        print("💡 Создай .env в корне week4 с этими переменными")
        exit(1)
    
    print(f"🔑 Пользователь: {USER}")
    print(f"🔑 Пароль: {'*' * len(PASSWORD)} (скрыт)")
    print(f"🌐 Хост: {HOST}")
    
    # Подключаемся
    client, sftp = connect_sftp(HOST, USER, PASSWORD)
    
    if not client:
        exit(1)
    
    # Тест: загружаем README
    with open("test_secure.txt", "w") as f:
        f.write("Это тестовый файл из безопасного скрипта.\n")
    
    upload_file(sftp, "test_secure.txt", "/tmp/test_secure.txt")
    
    # Закрываем
    sftp.close()
    client.close()
    print("\n✅ Соединение закрыто")
