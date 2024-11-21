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
    - python3 -m venv ~/.venvs/lichois
    - source ~/.venvs/lichois/bin/activate  # On Windows use `\.venvs\lichois\Scripts\activate`

3. Install the dependencies:
    - pip install -r requirements.txt

4. Set up the database:
    - python manage.py makemigrations_all

5. Management Commands
- python3 manage.py update_application_status
- python3 manage.py run_app_commands citizenship
- python3 manage.py run_app_commands workresidentpermit  
- python3 manage.py populate_renewal_replacement_applications 

6. Create a superuser (optional, for accessing the Django admin interface):
    - python manage.py createsuperuser

7. Run the development server:
    - python manage.py runserver

8. Data population commands:
   - populate_appeal_attachments
   - populate_appeal
   - populate_cancellation_attachments
   - populate_cancellation
   - populate_emergency_attachments
   - populate_emergency
   - populate_exemption_attachments
   - populate_exemption_variation
   - populate_exemption
   - populate_res_attachments
   - populate_res_only_replacement
   - populate_res_only
   - populate_variation_attachments
   - populate_work_attachments
   - populate_work_only_replacement
   - populate_work_only
   - populate_work_variation
   - populate_work_res_attachments
   - populate_work_res_data
   - populate_work_res_variation
   - populate_visa_permit
   - populate_visa_attachments
   - populate_travel_certificate
   - populate_travel_attachments
   - populate_permanent_residence_attachments
   - populate_permanent_residence_replacements
   - populate_permanent_residence_returns
   - populate_permanent_residence
   - populate_blue_card_attachments
   - populate_blue_card_replacement
   - populate_blue_card_returns
   - populate_blue_card
   - Exemption Renewals and Replacements: populate_exemption_final_applications --> populate_exemption_renewal_replacement_applications
   - Res Renewals and Replacements: populate_res_final_applications --> populate_res_renewal_replacement_applications
   - Work only Renewals and Replacements: populate_work_final_applications --> populate_work_renewal_replacement_applications
   - Work & Res Renewals and Replacements: populate_final_applications --> populate_renewal_replacement_applications

