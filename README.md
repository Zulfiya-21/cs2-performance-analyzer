
# CS2 Performance Analyzer

Веб-сервис на Python и FastAPI для анализа статистики игрока Counter-Strike 2.

## Возможности

- Добавление результатов матчей.
- Просмотр всех матчей.
- Поиск матча по ID.
- Расчёт общего K/D и Win Rate.
- Статистика отдельно по картам.
- Загрузка 10 реальных матчей из matches.json.
- Логирование событий.

## Технологии

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX

## Установка

Необходим Python 3.13 или совместимая версия.

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Установить зависимости:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Запуск приложения

Для разработки:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app_final:app --reload
```

Обычный запуск без автоматической перезагрузки:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app_final:app
```

После запуска открыть:

http://127.0.0.1:8000/docs

Для остановки сервера нажать Ctrl+C.

## API

- GET / — главная информация.
- GET /health — проверка работоспособности.
- GET /version — версия приложения.
- POST /matches — добавление матча.
- GET /matches — список матчей.
- GET /matches/{match_id} — поиск матча по ID.
- GET /statistics — общая статистика.
- GET /statistics/maps — статистика по картам.

## Данные

Файл matches.json содержит 10 матчей одного игрока:

- Dust 2 — 4 матча.
- Mirage — 3 матча.
- Nuke — 3 матча.

Данные автоматически загружаются при старте приложения.

Новые матчи, добавленные через API, хранятся в оперативной памяти и не записываются обратно в JSON.

## Переменные окружения

APP_NAME — название приложения.

Пример настройки находится в .env.example.

Для изменения названия в PowerShell перед запуском:

```powershell
$env:APP_NAME="My CS2 Analyzer"
```

Файл .env.example служит образцом и автоматически не загружается.

## Автоматические тесты

Установить зависимости для тестирования:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Запустить тесты:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Реализовано 5 автоматических тестов.

## Проверка и диагностика

После запуска приложения проверить:

http://127.0.0.1:8000/health

Ожидаемый ответ:

```json
{"status": "ok"}
```

Версия приложения:

http://127.0.0.1:8000/version

Ожидаемый ответ:

```json
{"version": "0.1.0"}
```

Логи приложения выводятся в терминал.

Если приложение не запускается:

1. Проверить, что зависимости установлены.
2. Проверить наличие файла matches.json.
3. Проверить сообщения об ошибках в терминале.
4. Проверить, свободен ли порт 8000.


## CI/CD

Проект использует GitHub Actions для автоматической проверки приложения.

При каждом push и pull request GitHub Actions:

1. Загружает исходный код проекта.
2. Устанавливает Python 3.13 и необходимые зависимости.
3. Запускает автоматические тесты с помощью pytest.
4. После успешного выполнения тестов создаёт artifact с файлами приложения.

Artifact включает:
- app_final.py
- matches.json
- requirements.txt
- README.md

Срок хранения artifact — 30 дней.

Результаты автоматических проверок доступны во вкладке Actions на GitHub.



## Запуск на Linux и macOS

Для запуска на Linux или macOS необходимо установить Python 3.13 или совместимую версию.

Клонировать репозиторий:

```bash
git clone https://github.com/Zulfiya-21/cs2-performance-analyzer.git
cd cs2-performance-analyzer
```

Создать виртуальное окружение:

```bash
python3 -m venv .venv
```

Установить зависимости:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Запустить приложение:

```bash
.venv/bin/python -m uvicorn app_final:app
```

После запуска открыть документацию API:

http://127.0.0.1:8000/docs

Для запуска автоматических тестов установить дополнительные зависимости:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
```

Выполнить тесты:

```bash
.venv/bin/python -m pytest -v
```

Для остановки сервера нажать Ctrl+C.
