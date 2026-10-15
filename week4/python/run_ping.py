#!/usr/bin/env python3
# ============================================
# PYTHON: ВЫЗЫВАЕТ BASH-СКРИПТ
# ============================================

import subprocess
import sys


def ping_servers(hosts):
    """Вызывает Bash-скрипт для проверки серверов."""
    cmd = ["bash", "scripts/ping_servers.sh"] + hosts
    
    print(f"📞 Вызов: {' '.join(cmd)}\n")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    
    # Выводим stdout
    print(result.stdout)
    
    # Выводим stderr (если есть)
    if result.stderr:
        print(f"⚠️  STDERR: {result.stderr}")
    
    return result.returncode


def main():
    hosts = sys.argv[1:] if len(sys.argv) > 1 else [
        "8.8.8.8", "1.1.1.1", "google.com", "192.168.99.99"
    ]
    
    print("=" * 60)
    print("🐍 PYTHON ВЫЗЫВАЕТ BASH")
    print("=" * 60)
    
    exit_code = ping_servers(hosts)
    
    print("=" * 60)
    if exit_code == 0:
        print("✅ Все серверы доступны")
    else:
        print(f"❌ Есть недоступные (код: {exit_code})")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
