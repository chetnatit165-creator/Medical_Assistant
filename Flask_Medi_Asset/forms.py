from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    DateField,
    TextAreaField,
    SubmitField,
    PasswordField,
    BooleanField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    EqualTo,
    ValidationError,
    NumberRange
)
from  Flask_Medi_Asset.dummy_data import User

class RegistrationForm(FlaskForm):

    username=StringField("Username",validators=[DataRequired(),Length(min=3,max=30)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    phone=StringField("Phone Number",validators=[DataRequired(),Regexp(r"^[0-9]{10}$",message="Enter a valid 10-digit phone number.")])
    password=PasswordField(" Password",validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password",message="Passwords must match.")])
    submit = SubmitField("Register")

    def validate_username(self,username):
       user=User.query.filter_by(username=username.data).first()
       if user:
             raise ValidationError("Username already exists.")

    def validate_email(self,email):
       user=User.query.filter_by(email=email.data.lower()).first()
       if user:
             raise ValidationError("Email already registered.")

class LoginForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    role = SelectField("Login As",choices=[("patient","Patient"),("doctor","Doctor"),("admin","Administrator")],validators=[DataRequired()])

    remember=BooleanField("Remember Me")
    submit=SubmitField("Login")

class DoctorRegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=3,max=30)])
    name=StringField("Doctor Name",validators=[DataRequired(),Length(max=100)])
    specialization=StringField("Specialization",validators=[DataRequired()])
    experience=IntegerField("Experience (Years)",validators=[DataRequired(),NumberRange(min=0,max=60)])

    email=StringField("Email",validators=[DataRequired(),Email()])
    phone=StringField("Phone Number",validators=[DataRequired(),Regexp(r"^[0-9]{10}$",message="Enter a valid 10-digit phone number.")])
    password=PasswordField("Temporary Password",validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password",message="Passwords must match.")])
    submit=SubmitField("Register Doctor")

def validate_username(self, username):
    user = User.query.filter_by(
        username=username.data.lower()
    ).first()

    if user:
        raise ValidationError("Username already exists.")


def validate_email(self, email):
    user = User.query.filter_by(
        email=email.data.lower()
    ).first()

    if user:
        raise ValidationError("Email already registered.")
class AppointmentForm(FlaskForm):

    doctor = SelectField(
        "Select Doctor",
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message="Please select a doctor.")
        ]
    )

    date = DateField(
        "Appointment Date",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Please select an appointment date.")
        ]
    )

    message = TextAreaField(
        "Reason for Visit",
        validators=[
            DataRequired(message="Please enter the reason for your visit."),
            Length(max=300)
        ]
    )

    submit = SubmitField("Book Appointment")
