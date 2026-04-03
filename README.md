# Task Management Application

## Features
- JWT Authentication
- Role-based system (SuperAdmin, Admin, User)
- Task assignment and tracking
- Completion report with worked hours
- Custom admin panel (HTML)

## Tech Stack
- Django
- Django REST Framework
- JWT Authentication
- SQLite

## Setup Instructions

1. Clone project
git clone <your_repo_link>

2. Install dependencies
pip install -r requirements.txt

3. Run migrations
python manage.py migrate

4. Run server
python manage.py runserver

## API Endpoints

- POST /api/token/
- GET /api/tasks/
- PUT /api/tasks/{id}/
- GET /api/tasks/{id}/report/

## Admin Panel
- Login via: http://127.0.0.1:8000/