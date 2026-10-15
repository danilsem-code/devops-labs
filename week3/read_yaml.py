# ============================================
# ЧТЕНИЕ YAML-КОНФИГА (как Ansible playbook)
# ============================================

import yaml


def load_yaml(filename):
    """Загружает YAML-файл."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден!")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Ошибка в YAML: {e}")
        return None


def print_playbook(data):
    """Выводит информацию о playbook."""
    print("=" * 60)
    print("📘 ANSIBLE PLAYBOOK")
    print("=" * 60)
    
    for play in data:
        print(f"\n🎯 Название: {play['name']}")
        print(f"   Хосты: {play['hosts']}")
        print(f"   become (sudo): {play.get('become', False)}")
        
        # Переменные
        if 'vars' in play:
            print(f"\n   📦 Переменные:")
            for key, value in play['vars'].items():
                print(f"      {key} = {value}")
        
        # Задачи
        print(f"\n   ✅ Задачи ({len(play['tasks'])}):")
        for i, task in enumerate(play['tasks'], 1):
            print(f"      {i}. {task['name']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("🔍 Загрузка playbook.yml...\n")
    
    data = load_yaml("playbook.yml")
    
    if data:
        print_playbook(data)
        print("✅ Playbook успешно разобран!")
