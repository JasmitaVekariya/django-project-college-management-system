# 🎓 College Management System

A web-based College Management System built with **Django 5**, enabling administrators and students to manage academic records, view results, and access department timetables — all through a clean, role-aware interface.

---

## 📖 Project Overview

The College Management System (CMS) is a full-stack web application that digitalises the everyday administrative and academic workflows of a college. It provides a centralised platform where:

- **Administrators (superusers)** can manage student profiles, enter and edit academic results, and oversee all records across every department.
- **Students** can register, maintain their own profile, view their semester results, and check their department timetable.

The system removes the need for manual paper-based processes, reduces data inconsistencies, and gives both staff and students instant access to accurate academic information.

---

## 🚨 Problem Statement

Traditional college administration relies heavily on manual record-keeping:

- Student data is scattered across spreadsheets or paper files, making it error-prone and hard to retrieve.
- Result entry is done separately for each subject with no validation, leading to incorrect marks or wrong subject assignments.
- Timetables are pinned on notice boards and are not easily accessible off-campus.
- There is no unified access-control model — any staff member can accidentally modify any record.

### Challenges in Existing Systems
| Challenge | Impact |
|-----------|--------|
| Manual data entry | High error rate in student records |
| No role separation | Unauthorised edits to sensitive data |
| Paper-based results | Delayed result disclosure |
| No digital timetable | Students miss schedule updates |

### Motivation
This project was built to demonstrate how a lightweight Django application can solve real institutional pain points without requiring expensive enterprise software.

---

## 💡 Solution Approach

### How the System Solves the Problem
- **Role-based access control** using Django's built-in `User` model and `is_superuser` flag ensures only administrators can create, edit, or delete records.
- **Data validation at the model layer** automatically derives a student's academic year from their semester and validates that entered subjects belong to the correct department and semester combination.
- **Centralised student profiles** link every record (results, timetable) to a single `Student` object, eliminating duplicate data.
- **Department-specific timetables** are served as dedicated views, accessible to anyone visiting the site.

### Key Design Decisions
- **Monolithic Django application** — keeps deployment simple, ideal for a single-institution deployment.
- **SQLite database** — zero-configuration setup for development; easily swappable for PostgreSQL in production.
- **Django's built-in authentication** — leverages proven, battle-tested login, logout, and session management.
- **Model-level business rules** — subject validity and semester-department consistency are enforced in `Result.save()`, not just in forms, preventing bad data regardless of how records are created.

### Benefits
- Zero additional infrastructure required to run locally.
- Easy to extend with new departments, subjects, or semesters by updating a single dictionary in the model.
- Clean separation between admin capabilities and student capabilities.

---

## 🏗️ Architecture Overview

The system follows a classic **MTV (Model-Template-View)** monolithic architecture provided by Django.

```
Browser
  │
  ▼
Django URL Router (cms/urls.py + student/urls.py)
  │
  ├─── cms/views.py  ──► index, timetable views
  │
  └─── student/views.py ──► student & result CRUD views
            │
            ▼
       student/models.py
        ├── Student  ──► db.sqlite3 (students table)
        └── Result   ──► db.sqlite3 (results table)
            │
            ▼
       Django Templates (HTML)
        ├── cms/templates/       (layout, index, login, timetables)
        └── student/templates/   (profile, list, result, form pages)
```

### Modules / Apps
| Module | Responsibility |
|--------|----------------|
| `cms` (project) | URL routing, index view, timetable views, settings |
| `student` (app) | Student and Result models, forms, views, and templates |
| Django Admin | Built-in admin panel for superuser data management |

### Communication
All communication is synchronous HTTP — standard Django request/response cycle. No message queues or external APIs are used.

---

## 🔄 Technical Flow

### User Request Flow

```
1. User visits the site
       │
       ▼
2. Django checks authentication (login_required decorator)
   - Not logged in  → redirect to /accounts/login/
   - Logged in      → continue
       │
       ▼
3. URL router matches the path and calls the appropriate view
       │
       ▼
4. View queries the database via Django ORM
   e.g. Student.objects.filter(user=request.user)
       │
       ▼
5. View passes the queryset to a template via context dict
       │
       ▼
6. Template renders HTML and returns HTTP response to browser
```

### Result Entry Flow (Admin only)

```
Admin submits ResultForm
  │
  ▼
Form validation (ResultForm.__init__ builds subject choices
  from Result.DEPARTMENT_SUBJECTS)
  │
  ▼
Result.save() enforces:
  - department matches student's department
  - semester matches student's semester
  - subject is valid for that department/semester
  │
  ▼
Record saved to db.sqlite3 → redirect to results list
```

---

## 📂 Project Structure

```
django-project-college-management-system/
│
├── requirements.txt              # Python dependencies
│
└── cms/                          # Django project root
    ├── manage.py                 # Django management entry point
    ├── db.sqlite3                # SQLite database (auto-created)
    │
    ├── cms/                      # Project-level package
    │   ├── settings.py           # Django settings (DB, auth, static files)
    │   ├── urls.py               # Root URL configuration
    │   ├── views.py              # Index, timetable, logout-redirect views
    │   ├── wsgi.py               # WSGI entry point for deployment
    │   └── asgi.py               # ASGI entry point (async support)
    │
    ├── student/                  # Student Django app
    │   ├── models.py             # Student and Result data models
    │   ├── views.py              # All student/result CRUD views
    │   ├── forms.py              # StudentForm, ResultForm, UserRegistrationForm
    │   ├── urls.py               # Student-scoped URL patterns
    │   ├── admin.py              # Django admin registrations
    │   ├── apps.py               # App configuration
    │   ├── migrations/           # Database migration files
    │   └── templates/            # App-level HTML templates
    │       ├── student_list.html
    │       ├── student_profile.html
    │       ├── student_form.html
    │       ├── student_confirm_delete.html
    │       ├── student_result.html
    │       ├── student_timetable.html
    │       ├── results_list.html
    │       ├── add_result.html
    │       ├── edit_result.html
    │       └── delete_result.html
    │
    ├── templates/                # Project-level HTML templates
    │   ├── layout.html           # Base layout (navbar, footer)
    │   ├── index.html            # Home/dashboard page
    │   ├── registration/
    │   │   ├── login.html
    │   │   ├── logout.html
    │   │   └── register.html
    │   └── timetable/
    │       ├── timetable_ce.html
    │       ├── timetable_it.html
    │       └── timetable_ec.html
    │
    ├── static/                   # Static assets
    │   ├── style.css
    │   └── images/logo.png
    │
    └── media/                    # User-uploaded files (student photos)
        └── photos/
```

---

## ⚙️ Features

| Feature | Details |
|---------|---------|
| 🔐 User Registration & Login | Custom registration form + Django's built-in authentication |
| 👤 Role-Based Access Control | Superuser (admin) vs regular student, enforced at view level |
| 🧑‍🎓 Student Profile Management | Create, view, edit, delete student profiles with photo upload |
| 📊 Academic Result Management | Admin enters results per subject; students view their own results |
| ✅ Subject Validation | Results are validated against department- and semester-specific subject lists |
| 📅 Year Auto-Calculation | Academic year is automatically derived from the student's current semester |
| 🗓️ Department Timetables | Dedicated timetable pages for CE, IT, and EC departments |
| 🔒 CSRF Protection | Django CSRF middleware active on all POST forms |
| 🖼️ Photo Upload | Student profile photos stored under `media/photos/` |
| 📈 Result Summary | Percentage calculation displayed on the student result page |

---

## 🌐 URL Endpoints

### Authentication

| URL | Method | Description |
|-----|--------|-------------|
| `/accounts/login/` | GET, POST | Login page |
| `/accounts/logout/` | POST | Log out current user |
| `/student/register/` | GET, POST | New user registration |
| `/logout-redirect/` | GET | Post-logout redirect handler |

### Student Management

| URL | Method | Access | Description |
|-----|--------|--------|-------------|
| `/student/` | GET | Authenticated | List all students (admin) or own profile (student) |
| `/student/create/` | GET, POST | Authenticated | Create a new student profile |
| `/student/<id>/` | GET | Authenticated | View a specific student profile |
| `/student/<id>/edit/` | GET, POST | Owner or Admin | Edit a student profile |
| `/student/<id>/delete/` | GET, POST | Admin only | Delete a student profile |
| `/student/<id>/timetable/` | GET | Authenticated | View student timetable |

### Result Management

| URL | Method | Access | Description |
|-----|--------|--------|-------------|
| `/student/<id>/result/` | GET | Authenticated | View results for a student |
| `/student/add-result/` | GET, POST | Admin only | Add a new result entry |
| `/student/results/` | GET | Authenticated | List all results (admin) or own results (student) |
| `/student/results/edit/<result_id>/` | GET, POST | Admin only | Edit an existing result |
| `/student/results/delete/<result_id>/` | POST | Admin only | Delete a result |

### Timetables & General

| URL | Method | Access | Description |
|-----|--------|--------|-------------|
| `/` | GET | Authenticated | Home / dashboard |
| `/timetable/ce/` | GET | Public | Computer Engineering timetable |
| `/timetable/it/` | GET | Public | Information Technology timetable |
| `/timetable/ec/` | GET | Public | Electronics & Communication timetable |
| `/admin/` | GET | Django admin | Django admin panel |

---

## 🔌 Services & Ports

This is a single-process Django application. When running the development server, the following default port is used:

| Service | Default Port | Notes |
|---------|-------------|-------|
| Django development server | `8000` | `python manage.py runserver` |
| SQLite database | N/A | File-based; no network port |
| Media files (photos) | served on `8000` | Served by Django in development |

---

## 🔐 Environment Variables

The project currently uses `settings.py` for configuration. For a production deployment, the following values **must** be moved to environment variables or a `.env` file (e.g., using `python-decouple` or `django-environ`):

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `SECRET_KEY` | Django cryptographic signing key | `your-secret-key-here` |
| `DEBUG` | Enable/disable debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | Database connection string (if switching from SQLite) | `postgres://user:pass@localhost/dbname` |
| `MEDIA_ROOT` | Absolute filesystem path for uploaded media | `/var/www/cms/media/` |

> ⚠️ **Security Note:** The `SECRET_KEY` currently hard-coded in `settings.py` must be replaced before any production deployment.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- pip (comes with Python)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/JasmitaVekariya/django-project-college-management-system.git
cd django-project-college-management-system

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
cd cms

# Apply all migrations to create the database schema
python manage.py migrate

# Create a superuser (administrator) account
python manage.py createsuperuser
```

### Running the Project

```bash
# Start the Django development server
python manage.py runserver
```

Open your browser and navigate to:

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home page (redirects to login if unauthenticated) |
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://127.0.0.1:8000/student/register/` | New user registration |

### First-Time Setup Checklist

1. Run the server and log in with your superuser credentials.
2. Navigate to `/student/create/` to add a student record.
3. Navigate to `/student/add-result/` to enter academic results for a student.
4. Log out and register as a regular student user to test the student-facing views.

---

## 🧪 Testing

### Running Unit Tests

```bash
cd cms
python manage.py test student
```

### Manual API Testing with Django Admin

1. Log in at `http://127.0.0.1:8000/admin/` with your superuser account.
2. Use the admin interface to directly create, inspect, and delete `Student` and `Result` records.

### Manual Testing with the Browser

Use the following flow to verify all features end-to-end:

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Visit `/` without logging in | Redirected to `/accounts/login/` |
| 2 | Register at `/student/register/` | Account created, redirected to student list |
| 3 | Create a student profile | Profile appears in `/student/` list |
| 4 | Log in as superuser and add a result | Result appears in `/student/<id>/result/` |
| 5 | Log in as student and view own result | Only own results visible |
| 6 | Visit `/timetable/ce/` | CE timetable page renders |

---

## 🛠️ Troubleshooting

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| `No module named 'django'` | Virtual environment not activated | Run `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows) |
| `django.db.utils.OperationalError: no such table` | Migrations not applied | Run `python manage.py migrate` |
| `ValueError: Invalid subject for ...` | Subject not in allowed list for that department/semester | Check `Result.DEPARTMENT_SUBJECTS` in `student/models.py` and use a valid subject name |
| `403 Forbidden` on POST forms | CSRF token missing | Ensure `{% csrf_token %}` is present inside all `<form>` tags |
| Photos not displaying | `MEDIA_URL`/`MEDIA_ROOT` not configured | Confirm `settings.py` has `MEDIA_URL = '/media/'` and the URL config includes `+ static(...)` |
| Login redirects to wrong page | `LOGIN_REDIRECT_URL` misconfigured | Check `LOGIN_REDIRECT_URL` in `settings.py` (currently set to `'/'`) |
| `TemplateDoesNotExist` error | Template not found in configured dirs | Verify `TEMPLATES[0]['DIRS']` in `settings.py` points to the correct templates folder |

---

## 📈 Future Improvements

| Area | Planned Enhancement |
|------|---------------------|
| 🔔 Notifications | Email or in-app alerts when results are published |
| 📊 Analytics Dashboard | Visual charts for department-wise and semester-wise performance |
| 📱 Mobile Responsive UI | Integrate Tailwind CSS (already in requirements) for a fully responsive layout |
| 🔒 Production Security | Move `SECRET_KEY` to environment variables; enable `HTTPS`; set `DEBUG=False` |
| 🗄️ PostgreSQL Support | Replace SQLite with PostgreSQL for multi-user production deployments |
| 📅 Dynamic Timetables | Store timetables in the database instead of static HTML files |
| 🧑‍🏫 Staff/Faculty Role | Add a Faculty role between Student and Superuser for result entry |
| 🔑 Password Reset | Implement email-based password reset using Django's `PasswordResetView` |
| 🐳 Docker Support | Containerise the application for one-command deployment |
| 🌐 REST API | Expose a JSON REST API using Django REST Framework for mobile app integration |

---

## 🤝 Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/django-project-college-management-system.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and ensure existing tests still pass:
   ```bash
   python manage.py test student
   ```
5. **Commit** with a clear message:
   ```bash
   git commit -m "feat: add email notification for new results"
   ```
6. **Push** to your fork and open a **Pull Request** against the `main` branch.

### Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Keep views thin — business logic belongs in models or forms.
- Write docstrings for any new model methods or utility functions.

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Jasmita Vekariya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```