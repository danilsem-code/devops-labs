# ============================================
# ФАЙЛОВЫЙ МЕНЕДЖЕР (os)
# Управляем файлами и папками из Python
# ============================================

import os
import datetime


def show_directory(path="."):
    """Показывает содержимое папки."""
    print(f"\n📁 Содержимое папки: {os.path.abspath(path)}")
    print("-" * 70)
    
    if not os.path.exists(path):
        print(f"❌ Путь не существует: {path}")
        return
    
    items = os.listdir(path)
    
    for item in sorted(items):
        full_path = os.path.join(path, item)
        
        if os.path.isdir(full_path):
            icon = "📁"
            size = "<DIR>"
        else:
            icon = "📄"
            size = f"{os.path.getsize(full_path)} B"
        
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
        mtime_str = mtime.strftime("%Y-%m-%d %H:%M")
        
        print(f"{icon} {item:<30} {size:>10}  {mtime_str}")
    
    print("-" * 70)
    print(f"Всего: {len(items)} объектов")


def create_backup_folder():
    """Создаёт папку для бэкапов с датой."""
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"backup_{date}"
    
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Создана папка: {folder}")
    return folder


def clean_old_files(folder, days=30):
    """Удаляет файлы старше N дней."""
    if not os.path.exists(folder):
        print(f"❌ Папка {folder} не существует")
        return
    
    now = datetime.datetime.now()
    deleted = 0
    
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)
        
        if os.path.isfile(full_path):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
            age = (now - mtime).days
            
            if age > days:
                os.remove(full_path)
                print(f"🗑️  Удалён: {item} (возраст: {age} дней)")
                deleted += 1
    
    print(f"\n✅ Удалено файлов: {deleted}")


def get_disk_usage(path="/"):
    """Показывает использование диска."""
    stat = os.statvfs(path) if hasattr(os, 'statvfs') else None
    
    # Для macOS используем subprocess (statvfs не везде работает)
    if stat is None:
        import subprocess
        result = subprocess.run(["df", "-h", path], capture_output=True, text=True)
        print(result.stdout)
    else:
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bfree * stat.f_frsize
        used = total - free
        percent = (used / total) * 100
        print(f"💾 Диск {path}:")
        print(f"   Всего:  {total / (1024**3):.2f} GB")
        print(f"   Занято: {used / (1024**3):.2f} GB ({percent:.1f}%)")
        print(f"   Свободно: {free / (1024**3):.2f} GB")


if __name__ == "__main__":
    print("=" * 70)
    print("ФАЙЛОВЫЙ МЕНЕДЖЕР (модуль os)")
    print("=" * 70)
    
    # 1. Показываем текущую папку
    show_directory(".")
    
    # 2. Создаём папку для бэкапов
    backup_dir = create_backup_folder()
    
    # 3. Чистим старые файлы (если есть)
    clean_old_files(".", days=365)  # Не удалит ничего, если файлы свежие
    
    # 4. Показываем использование диска
    print("\n" + "=" * 70)
    get_disk_usage("/")
