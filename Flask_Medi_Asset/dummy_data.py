from  flask_login import UserMixin
from datetime import datetime
from Flask_Medi_Asset import db


class User(UserMixin,db.Model):
    __tablename__ = "users"
    
    id =db.Column(db.Integer,primary_key=True)
    
    username=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    phone=db.Column(db.String(15),nullable=False)
    password=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(20),nullable=False,default="patient")
    is_active=db.Column(db.Boolean,default=True,nullable=False)
    appointments=db.relationship("Appointment",backref="patient",lazy=True,cascade="all,delete-orphan")
    doctor_profile=db.relationship("Doctor",back_populates="user",uselist=False,cascade="all, delete-orphan")

    def __repr__(self):
       return f"<User {self.username} ({self.role})>"


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )
    user_id=db.Column(
	db.Integer,
	db.ForeignKey("users.id"),
	unique=True,
	nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    experience = db.Column(
        db.Integer,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    user = db.relationship("User",back_populates="doctor_profile")

    appointments = db.relationship(
        "Appointment",
        backref="doctor",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Doctor {self.name}>"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    def __repr__(self):
        return (
                f"<Appointment "
                f"Patient={self.patient.username},"
                f"Doctor={self.doctor.name},"
                f"Date={self.appointment_date}>" )

    @property
    def date(self):
        return self.appointment_date

    @property
    def doctor_name(self):
        return self.doctor.name if self.doctor else ""

