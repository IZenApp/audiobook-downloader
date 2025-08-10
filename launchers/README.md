# 🚀 Launchers

Папка с лаунчерами для запуска разных интерфейсов программы.

## 📁 Содержимое

- **`console.py`** - Консольная версия с Rich UI
- **`gui_launcher.py`** - Графический интерфейс на Tkinter

## 🔧 Использование

Файлы запускаются через обертки в корневой папке:

```bash
# Из корневой папки проекта
python console.py        # Запускает launchers/console.py
python gui_launcher.py   # Запускает launchers/gui_launcher.py
```

Или напрямую:

```bash
# Прямой запуск
python launchers/console.py
python launchers/gui_launcher.py
```

## 🎯 Рекомендации

- **Новички**: Используйте обертки из корня (`python console.py`)
- **Опытные**: Можете запускать напрямую из этой папки
- **Автоматизация**: Используйте bash скрипты из `scripts/`
