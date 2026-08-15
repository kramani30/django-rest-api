# Django REST API

A simple task management REST API built with Django and Django REST Framework, featuring full CRUD operations, search, filtering, and ordering.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /api/tasks/ | List all tasks |
| POST | /api/tasks/ | Create a task |
| GET | /api/tasks/{id}/ | Retrieve a task |
| PUT | /api/tasks/{id}/ | Update a task |
| PATCH | /api/tasks/{id}/ | Partial update |
| DELETE | /api/tasks/{id}/ | Delete a task |
| GET | /api/tasks/by_status/?status=done | Filter by status |

## Running Locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/` to use the browsable API.

## Running Tests

```bash
python manage.py test api.tests
```

## Tech Stack

- Python 3.11+
- Django 4.2+
- Django REST Framework
- SQLite
- GitHub Actions CI/CD