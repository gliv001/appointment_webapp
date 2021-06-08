from flask_login import UserMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import datetime
from . import db


class UserLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userLevelId = db.Column(db.Integer, ForeignKey(UserLevel.level))
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    creationDate = db.Column(db.DateTime, default=datetime.now())


class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey(Users.id))
    email = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)
    loginTime = db.Column(db.DateTime, default=datetime.now())


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Numeric(precision=6, scale=2), default=0)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(64), nullable=False)
    serviceId = db.Column(db.Integer, ForeignKey(Service.id), nullable=True)
    employeeId = db.Column(db.Integer, ForeignKey(Employees.id), nullable=True)
    apptDateTime = db.Column(db.DateTime, default=datetime.now)
    tips = db.Column(db.Numeric(precision=6, scale=2), default=0)
    total = db.Column(db.Numeric(precision=6, scale=2), default=0)
    __table_args__ = (
        UniqueConstraint("employeeId", "apptDateTime", name="_employee_appt_uc"),
    )
