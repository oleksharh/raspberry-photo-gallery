# Backend API Setup Guide

## 1. Create and Activate Virtual Environment
On Windows, navigate to the backend directory (or your chosen project folder) and run:

```bash
python -m venv <name_of_venv>
```

Activate the virtual environment, you should be in the same directory as venv:
```bash
<name_of_venv>\Scripts\activate
```

Ensure you are in the directory where the virtual environment was initialized.

---

## 2. Install Dependencies
After activating the virtual environment, install the required dependencies:
```bash
pip install -r requirements.txt
```
This will install all necessary libraries for the project.

---

## 3. Database Migrations
Generate and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
Ensure that you have configured your `settings.py` properly and created a `.env` file with required environment variables.

---

## 4. Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```
Follow the link provided in the terminal to access the API.

---

## 5. Tweaking the API
Modify settings as needed to better fit your requirements. Adjust configurations in `settings.py` and `.env` where necessary.

---

You're now ready to develop and refine your API!

