# Theater System

Система управління театром для бронювання квитків та управління виставами.

## Технології

- Python 3.11
- Django 5.0
- PostgreSQL 15
- Redis 7
- Celery
- Nginx
- Docker

## Встановлення

1. Клонуйте репозиторій:
```bash
git clone https://github.com/yourusername/theater_system.git
cd theater_system
```

2. Створіть файл .env в корені проекту:
```bash
DEBUG=1
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://postgres:postgres@db:5432/theater_db
REDIS_URL=redis://redis:6379/0
```

3. Запустіть проект через Docker Compose:
```bash
docker-compose up --build
```

4. Застосуйте міграції:
```bash
docker-compose exec web python manage.py migrate
```

5. Створіть суперкористувача:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Розробка

1. Встановіть pre-commit хуки:
```bash
pip install pre-commit
pre-commit install
```

2. Запустіть тести:
```bash
docker-compose exec web pytest
```

## Структура проекту

```
theater_system/
├── core/            # Базові моделі та утиліти
├── shows/           # Управління виставами
├── halls/           # Управління залами
├── bookings/        # Система бронювання
├── payments/        # Платіжна система
├── users/           # Управління користувачами
└── notifications/   # Система сповіщень
```

## API Документація

Swagger UI доступний за адресою: http://localhost:8000/api/docs/

## Ліцензія

MIT
