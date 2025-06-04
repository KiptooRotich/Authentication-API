# Django Authentication API

A secure and customizable user authentication system built with Django and Django REST Framework.

## Features

* User registration with email verification
* Token-based login/logout (DRF token authentication)
* Profile view and update (first name, last name, profile picture, location)
* Password reset via email
* Account deactivation and reactivation

## Technologies Used

* Django 5.2.1
* Django REST Framework
* PostgreSQL
* Python 3.12

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd auth_api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv virtual
source virtual/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

## API Endpoints

| Endpoint                                     | Method  | Description                  |
| -------------------------------------------- | ------- | ---------------------------- |
| `/api/auth/register/`                        | POST    | Register a new user          |
| `/api/auth/login/`                           | POST    | Login and receive auth token |
| `/api/auth/logout/`                          | POST    | Logout (requires token)      |
| `/api/auth/profile/`                         | GET/PUT | View or update user profile  |
| `/api/auth/email-verify/`                    | GET     | Email verification link      |
| `/api/auth/request-reset-password/`          | POST    | Request password reset email |
| `/api/auth/password-reset/<uidb64>/<token>/` | POST    | Reset password               |
| `/api/auth/deactivate/`                      | POST    | Deactivate account           |
| `/api/auth/reactivate/`                      | POST    | Reactivate account           |

## License

MIT License

Copyright (c) 2025 Kiptoo Rotich
