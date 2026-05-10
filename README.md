# dwi.ma

Milestone 1 foundation for the dwi.ma MVP.

## Stack

- Python 3.12+
- Django 5
- Django Ninja
- PostgreSQL
- Celery + Redis
- Bootstrap 5 templates

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment file:
   ```bash
   cp .env.example .env
   ```
4. Update `.env` values for your local PostgreSQL/Redis.
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
7. Run web server:
   ```bash
   python manage.py runserver
   ```
8. Run Celery worker:
   ```bash
   celery -A config worker -l info
   ```

## Project apps

- accounts
- wallet
- payments
- whatsapp
- documents
- audio
- assistant
- notifications
- core

## Tests

```bash
pytest
```
