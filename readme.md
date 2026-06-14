# TeamFinder

TeamFinder — веб-приложение для поиска участников в проектные команды. Пользователи могут регистрироваться, заполнять профиль, добавлять навыки, создавать проекты и присоединяться к проектам других участников.

## Технологии

* Python
* Django
* PostgreSQL
* Docker Compose
* HTML
* CSS
* JavaScript

## Локальный запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/dshchd/team-finder-ad.git
cd team-finder-ad
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

Активация окружения:

Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

Windows cmd:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `.env_example` в `.env`:

```bash
cp .env_example .env
```

Пример содержимого `.env`:

```env
DJANGO_SECRET_KEY=change_for_safety
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=team_finder
POSTGRES_USER=team_finder
POSTGRES_PASSWORD=team_finder
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TASK_VERSION=2
```

Описание переменных:

| Переменная           | Описание                        |
| -------------------- | ------------------------------- |
| DJANGO_SECRET_KEY    | Секретный ключ Django           |
| DJANGO_DEBUG         | Режим отладки                   |
| DJANGO_ALLOWED_HOSTS | Разрешённые хосты через запятую |
| POSTGRES_DB          | Название базы данных            |
| POSTGRES_USER        | Пользователь PostgreSQL         |
| POSTGRES_PASSWORD    | Пароль PostgreSQL               |
| POSTGRES_HOST        | Хост PostgreSQL                 |
| POSTGRES_PORT        | Порт PostgreSQL                 |
| TASK_VERSION         | Номер варианта шаблонов         |

### 5. Запуск PostgreSQL через Docker Compose

```bash
docker compose up -d
```

Остановить контейнеры:

```bash
docker compose down
```

### 6. Применение миграций

```bash
python manage.py migrate
```

### 7. Загрузка тестовых данных

В репозитории присутствует файл `test_data.json` с тестовыми пользователями, навыками и проектами.

После применения миграций загрузите данные:

```bash
python manage.py loaddata test_data.json
```

Будут созданы тестовые пользователи, навыки и проекты для проверки функциональности приложения.

### 8. Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:8000
```

## Тестовые пользователи

После загрузки `test_data.json` доступны следующие аккаунты:

| Email                             | Пароль       |
| --------------------------------- | ------------ |
| tchertkovadasha@yandex.ru         | loll         |
| maxim@example.com                 | maxim        |
| elizaveta@example.com             | elizabeth123 |
| artem@example.com                 | artem        |

## Проверка качества кода

```bash
python manage.py check
python manage.py makemigrations
flake8 users projects team_finder manage.py --exclude=migrations --max-line-length=100
isort users projects team_finder manage.py --check-only
```
