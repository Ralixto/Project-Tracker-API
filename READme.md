# Project Tracker API

A REST API built with Django REST Framework supporting user authentication,
projects, task, task assignments and much more.

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL (production)
- JWT Authentication (simplejwt)

## Running Locally

1. Clone the repo
   git clone https://github.com/Ralixto/Project-Tracker-API.git
   cd projecttrackerapi

2. Create and activate a virtual environment
   python -m venv .venv
   .venv\Scripts\activate  # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Run migrations
   python manage.py migrate

5. Start the server
   python manage.py runserver

## API Endpoints

### Auth
- POST /api/register/
- POST /api/token/
- POST /api/token/refresh/

### project
- GET /project/
- POST /project/
- GET /project/{id}/
- PUT /project/{id}/
- PATCH /project/{id}/
- DELETE /project/{id}/

### task
- GET /task/
- POST /task/
- GET /task/{id}/
- PUT /task/{id}/
- PATCH /task/{id}/
- DELETE /task/{id}/

### Task Assignment
- GET /task-assignment/
- POST /task-assignment/
- GET /task-assignment/{id}/
- PUT /task-assignment/{id}/
- PATCH /task-assignment/{id}/
- DELETE /task-assignment/{id}/

## API Documentation
Swagger UI available at /api/docs/ after running the server.

## Running Tests
pytest