# EduCore Base Platform

A Modular and Reusable Education Management Platform.

## Installation

1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate` or `.\venv\Scripts\activate` on Windows
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill the variables.
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
