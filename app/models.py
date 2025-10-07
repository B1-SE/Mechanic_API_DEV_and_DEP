from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from app.extensions import db

# Create a base class for models
class Base(DeclarativeBase):
    pass

# association table
Service_Mechanic = db.Table(
    "service_mechanic",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"), primary_key=True),
)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    dob = db.Column(db.Date)                       # use db.Date (not db.date)
    password = db.Column(db.String(255), nullable=False)

    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)
    service_date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    customer = db.relationship("Customer", back_populates="service_tickets")
    mechanics = db.relationship("Mechanic", secondary=Service_Mechanic, back_populates="service_tickets")

class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)

    service_tickets = db.relationship("ServiceTicket", secondary=Service_Mechanic, back_populates="mechanics")