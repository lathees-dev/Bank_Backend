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
```

## 📁 Related Problem Set
See problems.md for the complete set of backend tasks and their solution links.

---

### 1. 🔐 Caesar Cipher – Encoding & Decoding  
🔗 [GitHub Repo](https://github.com/lathees-dev/Caesar-Cipher)

Encrypt and decrypt text using Caesar Cipher with dynamic shift support.

---

### 2. 💰 Indian Currency Formatter  
🔗 [GitHub Repo](https://github.com/lathees-dev/INR-Formatter)

Convert float numbers to Indian currency format (e.g., `12,34,567.89`).

---

### 3. 🧬 Merging Overlapping Lists  
🔗 [GitHub Repo](https://github.com/lathees-dev/Merge-List)

Combine two custom-formatted lists based on majority containment and index alignment.

---

### 4. 📉 Minimizing Financial Loss  
🔗 [GitHub Repo](https://github.com/lathees-dev/Minimize-Loss)

Given house prices, calculate the minimum financial loss by choosing buy-sell positions with guaranteed loss.

---
