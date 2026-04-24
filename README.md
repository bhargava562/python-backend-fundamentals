<div align="center">

# 🐍 Python Backend Fundamentals

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/python-backend-fundamentals?style=for-the-badge)

A structured, hands-on learning repository covering Python OOP, exception handling,
type hints, and advanced features — built day by day.

</div>

---

## 📁 Repository Structure

```
python-backend-fundamentals/
├── Day-1/
│   ├── myenv/                    ← virtual environment (not tracked by git)
│   ├── user.py                   ← Classes & Objects
│   ├── inheritance.py            ← Inheritance & Polymorphism
│   ├── decorators.py             ← @property, @staticmethod, @classmethod
│   ├── type_hints.py             ← Type Annotations
│   ├── exceptions.py             ← Exception Handling
│   ├── comprehensions.py         ← List & Dict Comprehensions
│   ├── context_managers.py       ← Context Managers
│   ├── lambda_map_filter.py      ← Lambda, map, filter, reduce
│   ├── args_kwargs.py            ← *args & **kwargs
│   └── README.md                 ← Day-1 concepts & learnings
└── README.md                     ← you are here
```

---

## 🗓️ Progress Tracker

| Day | Topics Covered | Status |
|-----|---------------|--------|
| [Day 1](./Day-1/README.md) | OOP · Inheritance · Decorators · Type Hints · Exceptions · Comprehensions · Context Managers · Lambda · *args/**kwargs | ✅ Complete |

---

## ⚙️ Setup Instructions

### Prerequisites

![Python](https://img.shields.io/badge/Requires-Python%203.10+-blue?style=flat-square&logo=python)
![Git](https://img.shields.io/badge/Requires-Git-orange?style=flat-square&logo=git)

```bash
python --version    # should be 3.10 or higher
git --version
```

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/bhargava562/python-backend-fundamentals.git
cd python-backend-fundamentals
```

---

### 2️⃣ Navigate to a Day's Folder

```bash
cd Day-1
```

---

### 3️⃣ Create & Activate the Virtual Environment

**macOS / Linux**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

**Windows**
```bash
python -m venv myenv
myenv\Scripts\activate
```

> Your terminal prompt will show `(myenv)` once activated.

---

### 4️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install mypy
```

> No third-party packages needed for Day-1 — everything uses Python's standard library.

---

### 5️⃣ Run Any File

```bash
python user.py
python exceptions.py
python args_kwargs.py
# ... and so on
```

---

### 6️⃣ Deactivate When Done

```bash
deactivate
```

---

### 7️⃣ Type-check with mypy (optional)

```bash
mypy type_hints.py
mypy decorators.py
```

---

## 🤝 Contributing

This is a personal learning repository. Feel free to fork it and follow the same day-by-day structure for your own backend journey.

---

<div align="center">
Made with ❤️ while learning Python — Chennai, India
</div>