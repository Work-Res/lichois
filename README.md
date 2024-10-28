# Django Project

This is a Django project. Follow the instructions below to set up and run the project on your local machine.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

## Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:Work-Res/lichois.git
   cd lichois


2. Create a virtual environment (optional but recommended):
    python3 -m venv ~/.venvs/lichois
    source ~/.venvs/lichois/bin/activate  # On Windows use `\.venvs\lichois\Scripts\activate`

3. Install the dependencies:
    pip install -r requirements.txt

4. Set up the database:
    python manage.py makemigrations_all

6 . populate data for apps
    python3 manage.py update_application_status
    python3 manage.py run_app_commands citizenship
    python3 manage.py run_app_commands workresidentpermit


5. Create a superuser (optional, for accessing the Django admin interface):
    python manage.py createsuperuser

6. Run the development server:
    python manage.py runserver


