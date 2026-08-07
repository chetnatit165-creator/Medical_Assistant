
from Flask_Medi_Asset.forms import AppointmentForm,RegistrationForm,LoginForm,DoctorRegistrationForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template, redirect, url_for, flash
from Flask_Medi_Asset import app, db
from Flask_Medi_Asset.dummy_data import Appointment, Doctor,User
from flask_login import login_required,current_user,login_user,logout_user

@app.route("/")
def home():
    doctors = Doctor.query.all()
    return render_template("index.html", doctors=doctors)

@app.route("/register",methods=["GET","POST"])
def register():
   if current_user.is_authenticated:
    return redirect(url_for("home"))

   form = RegistrationForm()

   if form.validate_on_submit():
       hashed_password=generate_password_hash(form.password.data)

       user=User(username=form.username.data,email=form.email.data.lower(),phone=form.phone.data,password=hashed_password,role="patient")

       db.session.add(user)
       db.session.commit()

       flash("Account created successfully! Please login.","success")
       return redirect(url_for("login"))
   return render_template("register.html",title="Patient Registration",form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "patient":
            return redirect(url_for("patient_dashboard"))
        elif current_user.role == "doctor":
            return redirect(url_for("doctor_dashboard"))
        elif current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data,
            role=form.role.data,
        ).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            flash(f"Welcome, {user.username}!", "success")

            if user.role == "patient":
                return redirect(url_for("patient_dashboard"))
            elif user.role == "doctor":
                return redirect(url_for("doctor_dashboard"))
            elif user.role == "admin":
                return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username, password, or role.", "danger")

    return render_template(
        "login.html",
        title="Login",
        form=form,
    )
@app.route("/doctors")
def doctor_list():
    doctors = Doctor.query.all()
    return render_template("doctors.html", doctors=doctors)


@app.route("/appointments")
@login_required
def appointment_list():
    if current_user.role != "patient":
        flash("Access denied.", "danger")
        return redirect(url_for("home"))

    appointments = Appointment.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "appointments.html",
        appointments=appointments,
    )


@app.route("/appointment/new", methods=["GET", "POST"])
@app.route("/appointment/new", methods=["GET", "POST"])
@login_required
def new_appointment():
    if current_user.role != "patient":
        flash("Only patients can book appointments.", "danger")
        return redirect(url_for("home"))

    doctors = Doctor.query.all()

    if not doctors:
        flash("No doctors are available.", "warning")
        return redirect(url_for("doctor_list"))

    form = AppointmentForm()

    form.doctor.choices = [(0, "--Select Doctor --")] + [
        (doctor.id, doctor.name)
        for doctor in doctors
    ]

    if form.validate_on_submit():
        if form.doctor.data == 0:
            flash("Please select a doctor.", "danger")
            return render_template(
                "appointment_form.html",
                title="Book Appointment",
                form=form
            )

        appointment = Appointment(
            appointment_date=form.date.data,
            message=form.message.data,
            doctor_id=form.doctor.data,
            user_id=current_user.id
        )

        db.session.add(appointment)
        db.session.commit()

        flash("Appointment booked successfully!", "success")

        return redirect(url_for("appointment_list"))

    return render_template(
        "appointment_form.html",
        title="Book Appointment",
        form=form
    )
@app.route("/patient/dashboard")
@login_required
def patient_dashboard():
    return render_template("patient_dashboard.html")

@app.route("/doctor/dashboard")
@login_required
def doctor_dashboard():
    return render_template("doctor_dashboard.html")

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.","success")
    return redirect(url_for("home"))
