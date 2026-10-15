# ============================================
# ОСНОВЫ SSH + PARAMIKO
# Подключаемся к серверу и выполняем команды
# ============================================

import paramiko
import sys


def connect_ssh(host, username, password=None, key_file=None, port=22):
    """
    Подключается к серверу по SSH.
    
    Параметры:
        host: IP или домен
        username: имя пользователя
        password: пароль (или None, если используем ключ)
        key_file: путь к приватному ключу
        port: порт (по умолчанию 22)
    
    Возвращает:
        SSH-клиент или None при ошибке
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_file:
            # Подключение по ключу
            key = paramiko.RSAKey.from_private_key_file(key_file)
            client.connect(host, port=port, username=username, pkey=key, timeout=10)
        else:
            # Подключение по паролю
            client.connect(host, port=port, username=username, password=password, timeout=10)
        
        print(f"✅ Подключено к {host}")
        return client
    
    except paramiko.AuthenticationException:
        print(f"❌ Ошибка аутентификации на {host}")
        return None
    except Exception as e:
        print(f"❌ Ошибка подключения к {host}: {e}")
        return None


def run_command(client, command):
    """
    Выполняет команду на сервере.
    
    Параметры:
        client: SSH-клиент
        command: команда для выполнения
    
    Возвращает:
        (stdout, stderr, exit_code)
    """
    stdin, stdout, stderr = client.exec_command(command)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    exit_code = stdout.channel.recv_exit_status()
    
    return output, error, exit_code


def main():
    # === НАСТРОЙКИ ===
    HOST = "localhost"          # Тренируемся на себе
    USERNAME = "danilsemenov"   # Твой логин на Mac
    # PASSWORD = "..."          # Пароль (если нужно)
    # KEY_FILE = "~/.ssh/id_rsa"  # Или ключ
    
    print("=" * 60)
    print("SSH + PARAMIKO: БАЗОВЫЙ ПРИМЕР")
    print("=" * 60)
    
    # 1. Подключаемся
    print(f"\n🔌 Подключение к {HOST}...")
    client = connect_ssh(HOST, USERNAME, password="")  # По ключу
    
    if not client:
        print("\n❌ Не удалось подключиться")
        print("💡 Убедись, что Remote Login включён в System Settings")
        sys.exit(1)
    
    # 2. Выполняем команды
    commands = [
        "hostname",
        "whoami",
        "date",
        "uname -a",
        "df -h /",
        "uptime",
    ]
    
    print("\n📋 Выполнение команд:")
    print("-" * 60)
    
    for cmd in commands:
        output, error, exit_code = run_command(client, cmd)
        
        print(f"\n$ {cmd}")
        if output:
            print(output.strip())
        if error:
            print(f"⚠️  {error.strip()}")
        if exit_code != 0:
            print(f"❌ Код выхода: {exit_code}")
    
    # 3. Закрываем соединение
    client.close()
    print("\n" + "=" * 60)
    print("✅ Соединение закрыто")


if __name__ == "__main__":
    main()
