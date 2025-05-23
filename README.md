# Spy Cat Agency — Backend API

This repository contains the backend implementation of the Spy Cat Agency management system, developed as part of a coding assessment. The application is built with **FastAPI** and provides full CRUD functionality for managing spy cats, missions, and their associated targets.

---

## Functionality Overview

* Manage spy cats with attributes such as name, experience, breed, and salary.
* Validate cat breeds using **TheCatAPI**.
* Create missions containing 1–3 targets; targets are created at mission initialization.
* Assign a single cat to a mission (1 mission per cat).
* Allow cats to submit and update notes per target (restricted if completed).
* Automatically complete missions once all targets are marked complete.
* Enforce business rules at the API level.

---

### Tech Stack

* **Python 3.11**
* **FastAPI** (REST framework)
* **SQLAlchemy** (ORM)
* **Pydantic** (validation)
* **SQLite** (local development database)
* **Requests** (external API integration)

---

### Local Setup

```bash
git clone https://github.com/bewayos/SCA-backend.git
cd spy-cat-agency-backend

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

### API Testing

A full **Postman collection** is available at:
**\[[LINK TO COLLECTION](https://artemyashchenko.postman.co/workspace/Artem-Yashchenko's-Workspace~35c77d8f-6985-4ec3-86ec-81245a12a52d/collection/43828896-f97a369a-2e70-4f89-bce7-a964b959899a?action=share&creator=43828896&active-environment=43828896-8a859cec-5652-4438-b40f-9481ca9ce1d0)]**
The collection includes:

* All main endpoints
* Validation edge cases
* Error handling scenarios

---

### Key API Endpoints

#### `/cats`

* `GET /cats` — List all spy cats
* `POST /cats` — Create a spy cat (breed validated via TheCatAPI)
* `GET /cats/{id}` — Retrieve specific cat
* `PATCH /cats/{id}` — Update salary
* `DELETE /cats/{id}` — Remove a cat

#### `/missions`

* `POST /missions` — Create a mission (with 1–3 targets)
* `PATCH /missions/{id}/assign` — Assign a cat
* `GET /missions` — List missions
* `GET /missions/{id}` — Retrieve specific mission
* `DELETE /missions/{id}` — Delete mission (only if unassigned)

#### `/missions/targets`

* `PATCH /targets/{id}/notes` — Update notes (only if target and mission are not complete)
* `PATCH /targets/{id}/complete` — Mark a target as complete (triggers mission completion check)

---

### Business Rules & Validations

* **Breed Validation:** Cat breeds are checked in real-time against [TheCatAPI](https://thecatapi.com/v1/breeds).
* **Mission Composition:** A mission must include between 1 and 3 targets at creation.
* **Target Restrictions:** Notes can’t be updated once the target or the mission is marked complete.
* **Mission Assignment:** Each cat can only be assigned to one mission at a time. Assigned missions cannot be deleted.

---

### Project Structure

```
app/
├── main.py         # Application entrypoint
├── models.py       # SQLAlchemy models
├── schemas.py      # Pydantic schemas
├── crud.py         # Business logic
├── database.py     # DB configuration
├── api/
│   ├── cats.py     # Cat-related routes
│   └── missions.py # Mission/Target-related routes
```
