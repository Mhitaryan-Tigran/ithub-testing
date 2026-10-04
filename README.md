# Тестирование. Проектирование тестов

Мхитарян Тигран Айказович, группа ИСП9. Контрольные точки 1–10.

| КТ | Папка | Тема | Отчёт |
|---|---|---|---|
| 1 | [kt01-manual](kt01-manual/) | Ручное тестирование веб-приложения «Сборщик контента»: 21 тест-кейс, 3 дефекта | docx |
| 2 | [kt02-files](kt02-files/) | CSV и JSON: средний балл с проверкой в pytest (найдено 16 ошибок в данных), сортировка супергероев | docx |
| 3 | [kt03-api](kt03-api/) | Базовый класс запросов и по 4 запроса к user и store на petstore.swagger.io | docx |
| 4 | [kt04-dog-api](kt04-dog-api/) | MindMap Dog API и по 5 тестов к каждой из 5 сущностей | docx |
| 5 | [kt05-allure-pydantic](kt05-allure-pydantic/) | Тесты petstore на httpx с Allure и моделями Pydantic | docx |
| 6 | [kt06-coverage-async](kt06-coverage-async/) | Асинхронный клиент API и покрытие тестами: 80% → 100% | docx |
| 7 | [kt07-async-tasks](kt07-async-tasks/) | Пять задач на асинхронные тесты: future, исключение, aiohttp, aiosqlite, поток | docx |
| 8 | [kt08-aiohttp-allure](kt08-aiohttp-allure/) | get_json на aiohttp, тесты с локальным сервером, покрытие и Allure | docx |
| 9 | [kt09-fastapi-profile](kt09-fastapi-profile/) | Тестовое задание: FastAPI-приложение с регистрацией и профилем, 18 асинхронных тестов | docx |
| 10 | [kt10-postgres-sql](kt10-postgres-sql/) | Тестовое задание: 5 SQL-запросов к PostgreSQL с автотестами | docx |

## Запуск

Python-работы:

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r kt09-fastapi-profile/requirements.txt
cd kt09-fastapi-profile && pytest -v
```

КТ10: `cd kt10-postgres-sql && npm install && node --test queries.test.mjs`.
