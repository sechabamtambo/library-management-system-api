# Library Management System API

A backend system for managing books, users, and checkouts, built with **Django** and **Django REST Framework (DRF)**. This project is part of the **ALX Backend Capstone Project**.

---

# Features
- User registration and authentication
- Add, update, and delete books
- Borrow and return books
- View all available and borrowed books
- Role-based permissions (admin vs user)

---

# Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (default), PostgreSQL (optional)
- **Authentication:** JWT / Session Authentication
- **Version Control:** Git & GitHub

---

# Project Structure
library-management-system-api/
│
├── config/        # Django project settings and URLs
├── library/       # Main app (models, serializers, views, urls)
├── env/           # Virtual environment (excluded in git)
└── manage.py
```

---

## ⚙️ Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/sechabamtambo/library-management-system-api.git
cd library-management-system-api
```

2. Create and activate virtual environment:
```bash
python -m venv env
# Windows (Git Bash):
source env/Scripts/activate
# Windows (PowerShell):
.\env\Scripts\Activate.ps1
# Mac/Linux:
source env/bin/activate
```

3. Install dependencies:
```bash
pip install django djangorestframework
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Run server:
```bash
python manage.py runserver


API Endpoints (Examples)

GET /api/books/ : List all books

POST /api/books/ : Add a new book

GET /api/books/{id}/ : Retrieve book details

PUT /api/books/{id}/ : Update book details

DELETE /api/books/{id}/ : Delete a book

Author

Sechaba Mtambo

GitHub: @sechabamtambo