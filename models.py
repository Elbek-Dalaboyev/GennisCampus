import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'GennisData')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def db_create_all():
    db.create_all()

class Auth(db.Model):
    __tablename__ = 'Auth'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    second_phone = Column(Integer)
    permission = Column(String)
    image_link = Column(String)
    subject = Column(String(120))
    why_subject = Column(String())
    locations = Column(Integer, ForeignKey('Locations.id'), nullable=False)

    def __init__(self, name, surname, email, password, phone, second_phone, permission, image_link, locations):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.phone = phone
        self.second_phone = second_phone
        self.permission = permission
        self.image_link = image_link
        self.locations = locations

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'second_phone': self.second_phone,
            'image_link': self.image_link,
            'location': self.locations
        }

class Groups(db.Model):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    students = Column(String, nullable=False)

    def __init__(self, subject, teacher, students):
        self.subject = subject
        self.teacher = teacher
        self.students = students

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Teachers(db.Model):
    __tablename__ = 'Teachers'
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    teacher = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Locations(db.Model):
    __tablename__ = 'Locations'
    id = Column(Integer, primary_key=True)
    loc = Column(String, nullable=False)
    student_list = db.relationship('Auth', backref='student_list')
