# 🧪 Tests

Тесты для проверки работоспособности программы.

## 📋 Файлы

- `test_core.py` - Основные тесты
- `__init__.py` - Инициализация тестов

## 🚀 Запуск тестов

### Все тесты
```bash
python -m pytest tests/ -v
```

### Конкретный тест
```bash
python -m pytest tests/test_core.py -v
```

### Прямой запуск
```bash
python tests/test_core.py
```

## 📊 Что тестируется

### ✅ test_parsing
- Загрузка списка книг
- Парсинг формата `Автор - Название`
- Проверка количества книг

### ✅ test_dependencies  
- Наличие всех зависимостей
- Импорт необходимых модулей
- Проверка установки пакетов

## 📈 Результаты

```
tests/test_core.py::test_parsing PASSED      [50%]
tests/test_core.py::test_dependencies PASSED [100%]

======================== 2 passed in 0.20s ========================
```

## 🔧 Отладка

```bash
# Подробный вывод
python -m pytest tests/ -v -s

# Остановка на первой ошибке
python -m pytest tests/ -x

# Покрытие кода
python -m pytest tests/ --cov=src
```

## 📋 Добавление тестов

1. Создайте файл `test_*.py`
2. Добавьте функции `test_*()`
3. Используйте `assert` для проверок

```python
def test_new_feature():
    assert True  # Ваша проверка
```
