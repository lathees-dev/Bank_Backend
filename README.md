# 🏦 Bank Backend – Loan Management System

This is a Django REST Framework (DRF)-powered backend for managing bank loans, EMIs, ledgers, and borrower data. Designed to streamline loan disbursement, track repayments, and compute remaining EMIs dynamically.

---

## 🚀 Features

- 🔐 Secure loan creation and borrower handling
- 📊 Ledger view with total, paid, and balance amount
- 📅 Auto-calculated EMIs left
- 📂 UUID-based endpoints for resource safety
- 💬 Django Admin + DRF APIs

---

## 🛠️ Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- SQLite (dev) / PostgreSQL (prod-ready)

---

## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/your-username/bank_backend.git
cd bank_backend

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
