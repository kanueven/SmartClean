# 🧹 SmartClean API

> ALX Software Engineering Capstone Project

A backend REST API for managing operations of a cleaning business — handling clients, cleaners, admins, jobs, quotes, and service-based pricing.

---

## 📌 Project Overview

SmartClean solves the real operational problems faced by cleaning businesses — missed jobs, manual scheduling, inconsistent pricing, and poor staff coordination. Most cleaning businesses rely on WhatsApp messages, sticky notes, and spreadsheets. This system replaces all of that with a structured, role-based API.

This project was built as a capstone submission for the **ALX Software Engineering Programme**.

---

## 👥 User Roles

Every user registers with a role. The role determines what they can see and do across the entire system.

| Role | What they can do |
|------|-----------------|
| **Admin** | Full access — manage users, cleaners, clients, jobs, services, generate quotes |
| **Client** | Create jobs, choose services, view their own jobs, accept quotes |
| **Cleaner** | View jobs assigned to them, mark jobs as completed |

A user cannot act outside their role. All endpoints enforce role-based access control using Django Groups.

---

## ✨ Features

- JWT authentication — register, login, token refresh
- Role-based access control using Django Groups
- Client profile management
- Cleaner profile management with availability tracking
- Service catalogue with base pricing
- Job lifecycle management with enforced status transitions
- Quote generation from service line items
- Client quote approval workflow
- Cleaner job completion
- Job cancellation with reason tracking
- Protection against deleting cleaners or clients with existing jobs
- Price snapshotting — quoted prices don't change if service prices are updated later

---

## 🔄 Job Lifecycle

Every job follows a strict flow. You cannot skip steps.

```
draft → quoted → scheduled → in_progress → completed
  ↓        ↓         ↓            ↓
cancelled cancelled cancelled   (cannot cancel)
```

| Status | Triggered by |
|--------|-------------|
| `draft` | Client creates a job |
| `quoted` | Admin generates a quote |
| `scheduled` | Client accepts the quote |
| `in_progress` | Admin starts the job |
| `completed` | Assigned cleaner marks it done |
| `cancelled` | Admin or job owner at any valid stage |

---

## 💰 Pricing

Pricing is derived entirely from **service types**. Each service has a `base_price`. When services are added to a job with a quantity, the price is **snapshotted** at that moment into `unit_price` on the `JobService` record.

This means:
- If Deep Clean is $150 today and changes to $200 tomorrow, existing quotes stay at $150
- The admin generates a quote by summing all `quantity × unit_price` on the job
- The client sees a full breakdown before accepting

---

## 🔒 Deletion Protection

- A **cleaner cannot be deleted** if they have jobs attached to them
- A **client cannot be deleted** if they have jobs attached to them  
- A **service cannot be deleted** if it is attached to any job — deactivate it instead
- A **job can only be deleted** if it is in `draft` status

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Framework | Django 4.2 |
| API | Django REST Framework |
| Authentication | JWT via `djangorestframework-simplejwt` |
| Database | SQLite (development) / PostgreSQL (production) |
| Deployment | Gunicorn + WhiteNoise |

---

## 📁 Project Structure

```
smartclean/
├── manage.py
├── requirements.txt
├── smartclean/
│   ├── settings.py
│   └── urls.py
└── apps/
    ├── accounts/        # Custom User model, JWT auth, group-based roles
    ├── clients/         # Client profiles, CRUD
    ├── cleaners/        # Cleaner profiles, availability, skills
    ├── services/        # Service catalogue, JobService through model
    └── jobs/            # Job lifecycle, quote generation, transitions
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smartclean.git
cd smartclean
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Assign the superuser to the admin group
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import Group
from accounts.models import User

u = User.objects.get(username='your_username')
group, _ = Group.objects.get_or_create(name='admin')
u.groups.add(group)
u.save()
```

### 7. Run the server
```bash
python manage.py runserver
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/register/` | Register a new user | Public |
| POST | `/api/auth/login/` | Login and get JWT tokens | Public |
| POST | `/api/auth/token/refresh/` | Refresh access token | Public |
| GET | `/api/auth/users/` | List all users | Admin |
| GET/PATCH | `/api/auth/users/<id>/` | View or update a user | Admin or own account |
| DELETE | `/api/auth/users/<id>/` | Deactivate a user | Admin |

### Clients
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/clients/` | List clients | Admin sees all, client sees self |
| POST | `/api/clients/` | Create client profile | Client or Admin |
| GET/PATCH | `/api/clients/<id>/` | View or update client | Admin or owner |
| DELETE | `/api/clients/<id>/` | Delete client | Admin only |

### Cleaners
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/cleaners/` | List cleaners | Admin sees all, cleaner sees self |
| POST | `/api/cleaners/` | Create cleaner profile | Cleaner or Admin |
| GET/PATCH | `/api/cleaners/<id>/` | View or update cleaner | Admin or owner |
| DELETE | `/api/cleaners/<id>/` | Delete cleaner | Admin only, blocked if jobs exist |

### Services
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/services/` | List active services | Public |
| POST | `/api/services/` | Create a service | Admin only |
| GET/PATCH | `/api/services/<id>/` | View or update service | GET public, others admin |
| DELETE | `/api/services/<id>/` | Delete service | Admin only, blocked if on a job |
| GET | `/api/services/job/<job_id>/` | List services on a job | Authenticated |
| POST | `/api/services/job/<job_id>/` | Add service to a job | Authenticated |
| DELETE | `/api/services/job/<job_id>/<id>/` | Remove service from job | Admin |

### Jobs
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/jobs/` | List jobs | Admin all, cleaner assigned, client own |
| POST | `/api/jobs/` | Create a job | Client or Admin |
| GET/PATCH | `/api/jobs/<id>/` | View or update job | Authenticated |
| DELETE | `/api/jobs/<id>/` | Delete job | Admin, draft only |
| POST | `/api/jobs/<id>/generate-quote/` | Generate quote from services | Admin only |
| POST | `/api/jobs/<id>/accept-quote/` | Accept quote | Job owner (client) |
| POST | `/api/jobs/<id>/start/` | Start job | Admin only |
| POST | `/api/jobs/<id>/complete/` | Mark job complete | Assigned cleaner only |
| POST | `/api/jobs/<id>/cancel/` | Cancel job | Admin or job owner |

---

## 🧪 Testing with Postman

### Typical workflow

**1. Register users**
```json
POST /api/auth/register/
{
    "username": "john_client",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123",
    "role": "client"
}
```

**2. Login and copy the access token**
```json
POST /api/auth/login/
{
    "username": "john_client",
    "password": "SecurePass123"
}
```

Add `Authorization: Bearer <access_token>` to all subsequent requests.

**3. Create client profile (logged in as client)**
```json
POST /api/clients/
{
    "phone_number": "07700900001",
    "address": "Kapsabet London"
    "special_instructions": "Please use omo products"
}
```

**4. Create a job (logged in as client)**
```json
POST /api/jobs/
{
    "title": "House Cleaning - 3 bed flat",
    "scheduled_date": "2026-03-10T09:00:00Z",
    "estimated_duration_hours": "03:00:00",
    "services": [1, 2]
}
```

**5. Generate quote (admin token)**
```
POST /api/jobs/1/generate-quote/
```

**6. Accept quote (client token)**
```
POST /api/jobs/1/accept-quote/
```

**7. Start job (admin token)**
```
POST /api/jobs/1/start/
```

**8. Complete job (assigned cleaner token)**
```
POST /api/jobs/1/complete/
```

---

## 🔑 Registration Roles

When registering, send one of these roles:

```json
{ "role": "client" }
{ "role": "cleaner" }
{ "role": "admin" }
```

---

## 📝 Notes

- Passwords must meet Django's default password validation rules
- Tokens expire after 24 hours — use `/api/auth/token/refresh/` to get a new one
- A user can only have one client or cleaner profile
- Services are public to read — any visitor can see the service catalogue
- Quoted prices are locked at the time of quote generation

---

## 👤 Author

Built by **[Rachael Gathoni]** as a capstone project for the **ALX Software Engineering Programme**.

---

