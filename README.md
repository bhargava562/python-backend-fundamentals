<div align="center">

# 🐍 Python Backend Fundamentals

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/bhargava562/python-backend-fundamentals?style=for-the-badge)

A structured, hands-on learning repository covering Python OOP, SQL, FastAPI, and production-grade data validation — built day by day.

</div>

---

## 📁 Repository Structure

```text
python-backend-fundamentals/
├── Day-1/ → Python Core (OOP, Decorators, Exceptions, Functional Programming)
├── Day-2/ → Git Fundamentals (Cheat Sheets, Workflow, Branching)
├── Day-3/ → SQL Mastery (Schema Design, Joins, Transactions, Normalization)
├── Day-4/ → FastAPI Basics (REST API CRUD, Path/Query Params, In-memory DB)
├── Day-5/ → Pydantic Mastery (Advanced Validation, CRUD Patterns, Nested Models)
├── Day-6/ → ORM & Advanced CRUD (SQLAlchemy, Database Models, Query Optimization)
├── Day-7/ → JWT Authentication (Token Management, Role-Based Access, Auth Routes)
├── Day-8/ → OAuth 2.0 Integration (Google OAuth, Session Management, Security Hardening)
└── README.md ← (You are here)
```

---

## 🗓️ Progress Tracker

| Day | Topics Covered | Status |
|-----|---------------|--------|
| [Day 1](./Day-1/README.md) | OOP · Inheritance · Decorators · Type Hints · Context Managers · Lambda | ✅ Complete |
| [Day 2](./Day-2/README.md) | Git Setup · Branching · Stashing · Conventional Commits · Undoing Changes | ✅ Complete |
| [Day 3](./Day-3/README.md) | SQL Schema · Joins · Aggregations · Advanced CTEs · Transactions · 3NF | ✅ Complete |
| [Day 4](./Day-4/README.md) | FastAPI CRUD · Swagger UI · Query Parameters · Global Error Handling | ✅ Complete |
| [Day 5](./Day-5/README.md) | Pydantic v2 · Custom Validators · Field Aliases · Nested Complex Models | ✅ Complete |
| [Day 6](./Day-6/README.md) | SQLAlchemy ORM · Database Models · Relationships · Query Optimization · CRUD Operations | ✅ Complete |
| [Day 7](./Day-7/README.md) | JWT Tokens · Access/Refresh Tokens · Role-Based Access · Auth Routes · Security Best Practices | ✅ Complete |
| [Day 8](./Day-8/README.md) | OAuth 2.0 · Google OAuth Integration · Session Management · Credential Protection · Security Hardening | ✅ Complete |

---

## ⚙️ Setup Instructions

### Prerequisites
- **Python:** 3.10 or higher
- **Git:** Installed and configured
- **Database:** MySQL/PostgreSQL (Optional for Day 3 SQL practice)

### 1️⃣ Clone & Navigate
```bash
git clone [https://github.com/bhargava562/python-backend-fundamentals.git](https://github.com/bhargava562/python-backend-fundamentals.git)
cd python-backend-fundamentals
```

### 2️⃣ Environment Setup
Each day's folder may have its own `requirements.txt`. For the later days (Day 4 & 5), ensure you install the dependencies:
```bash
# Example for Day 5
cd Day-5
python -m venv venv
# Windows: venv\Scripts\activate | macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Running Assignments
- **Day 1-2:** Run individual scripts (e.g., `python Day-1/user.py`).
- **Day 4:** Run the FastAPI server: `uvicorn app.main:app --reload`.
- **Day 5:** Run the validation demo: `python app/main.py`.

---

## 🤝 Contributing
This is a personal learning repository tracking my backend engineering journey. Feel free to fork it for your own structured learning path.

<div align="center">
Made with ❤️ while learning Python — Chennai, India
</div>
