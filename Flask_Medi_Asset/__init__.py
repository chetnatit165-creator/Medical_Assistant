import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash


app = Flask(__name__, instance_relative_config=True)


login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


app.config.from_mapping(
    SECRET_KEY='db67d6d60d597b700a207c6317186e5b',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(app.instance_path, 'site.db').as_posix()}"
)


os.makedirs(app.instance_path, exist_ok=True)


db_path = Path(app.instance_path, 'site.db')

if db_path.exists() and db_path.stat().st_size == 0:
    db_path.unlink()


db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    from Flask_Medi_Asset.dummy_data import User
    return db.session.get(User, int(user_id))


from Flask_Medi_Asset import routes


with app.app_context():

    from Flask_Medi_Asset.dummy_data import User, Doctor

    db.create_all()


    if User.query.filter_by(role="doctor").first() is None:

        sample_doctor_users = [

            User(
                username="johnsmith",
                email="john.smith@example.com",
                phone="5551234567",
                password=generate_password_hash("doctor123"),
                role="doctor"
            ),

            User(
                username="sarahwilson",
                email="sarah.wilson@example.com",
                phone="5559876543",
                password=generate_password_hash("doctor123"),
                role="doctor"
            )

        ]

        db.session.add_all(sample_doctor_users)
        db.session.commit()


        sample_doctors = [

            Doctor(
                name="Dr. John Smith",
                specialization="Cardiology",
                experience=15,
                email="john.smith@example.com",
                phone="5551234567",
                user_id=sample_doctor_users[0].id
            ),

            Doctor(
                name="Dr. Sarah Wilson",
                specialization="Dermatology",
                experience=10,
                email="sarah.wilson@example.com",
                phone="5559876543",
                user_id=sample_doctor_users[1].id
            )

        ]

        db.session.add_all(sample_doctors)
        db.session.commit()