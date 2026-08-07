# MediAsset — Flask/Jinja2 + Bootstrap 5.3 frontend

Drop-in templates and CSS for the MediAsset medical appointment system.

## Files

```
flask_frontend/
├── static/css/style.css        # theme (white / medical blue / light gray)
└── templates/
    ├── base.html               # layout, sticky navbar, flash messages, footer
    ├── _macros.html            # render_field, render_select, stat_card, avatar, ...
    ├── index.html  about.html  contact.html  404.html  doctors.html
    ├── login.html  register.html  change_password.html
    ├── patient_dashboard.html  appointment_form.html  appointments.html
    ├── patient_profile.html    edit_patient_profile.html
    ├── doctor_dashboard.html   doctor_appointments.html
    ├── doctor_profile.html     edit_doctor_profile.html
    ├── admin_dashboard.html    admin_appointments.html
    ├── doctor_register.html    manage_doctors.html   edit_doctor.html
    ├── manage_patients.html    edit_patient.html
    └── admin_profile.html      edit_admin_profile.html
```

Copy `templates/` and `static/` into your Flask app root.

## Required endpoint names (`url_for`)

| Endpoint | Path |
| --- | --- |
| `index` | `/` |
| `about` | `/about` |
| `contact` | `/contact` |
| `doctors` | `/doctors` |
| `register` / `login` / `logout` | `/register`, `/login`, `/logout` |
| `patient_dashboard` | `/patient/dashboard` |
| `new_appointment` | `/appointment/new` (optional `?doctor_id=`) |
| `appointments` | `/appointments` |
| `patient_profile` / `edit_patient_profile` | `/patient/profile`, `/patient/profile/edit` |
| `change_password` | `/change-password` |
| `doctor_dashboard` | `/doctor/dashboard` |
| `doctor_appointments` | `/doctor/appointments` |
| `doctor_profile` / `edit_doctor_profile` | `/doctor/profile`, `/doctor/profile/edit` |
| `admin_dashboard` | `/admin/dashboard` |
| `new_doctor` | `/admin/doctor/new` |
| `manage_doctors` | `/admin/doctors` |
| `edit_doctor` | `/admin/doctor/<int:doctor_id>/edit` |
| `delete_doctor` | `/admin/doctor/<int:doctor_id>/delete` (POST) |
| `manage_patients` | `/admin/patients` |
| `edit_patient` | `/admin/patient/<int:user_id>/edit` |
| `delete_patient` | `/admin/patient/<int:user_id>/delete` (POST) |
| `admin_appointments` | `/admin/appointments` |
| `admin_profile` / `edit_admin_profile` | `/admin/profile`, `/admin/profile/edit` |

## Context variables per template

- **index**: `doctor_count`, `patient_count`, `appointment_count`, `specialization_count`, `featured_doctors`
- **doctors**: `doctors`
- **patient_dashboard**: `upcoming_appointment`, `total_appointments`, `appointments`, `now`
- **appointments**: `appointments`, `now`
- **doctor_dashboard**: `doctor`, `today_appointments`, `today_appointments_count`, `total_patients`, `total_appointments`
- **doctor_appointments**: `appointments`, `now`
- **admin_dashboard**: `doctor_count`, `patient_count`, `appointment_count`, `today_count`, `recent_appointments`, `active_doctors`, `active_patients`, `specialization_count`, `week_count`, `now`
- **manage_doctors**: `doctors` · **manage_patients**: `patients` · **admin_appointments**: `appointments`, `now`
- **edit_doctor**: `form`, `doctor` · **edit_patient**: `form`, `patient`
- all form pages: `form` (Flask-WTF)

`Appointment` is expected to expose `doctor` and `patient` relationships
(`patient = db.relationship("User", backref="appointments")`).

Inject `now` and `current_year` globally:

```python
from datetime import datetime

@app.context_processor
def inject_globals():
    return {"now": datetime.utcnow(), "current_year": datetime.utcnow().year}
```

Register the 404 handler:

```python
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
```

## Form field names expected

- `RegistrationForm`: `username, email, phone, password, confirm_password, submit`
- `LoginForm`: `username, password, role, remember_me, submit`
- `DoctorRegistrationForm`: `username, name, specialization, experience, email, phone, password, confirm_password, submit`
- `AppointmentForm`: `doctor` (SelectField), `appointment_date` (DateTimeLocalField), `message` (TextAreaField), `submit`
- `ChangePasswordForm`: `current_password, new_password, confirm_password, submit`
- Profile forms: `username, email, phone, submit` (doctor: `name, specialization, experience, email, phone, submit`)

For `appointment_date`, use:

```python
from wtforms.fields import DateTimeLocalField
appointment_date = DateTimeLocalField("Appointment Date", format="%Y-%m-%dT%H:%M")
```
