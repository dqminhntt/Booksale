from flask_login import current_user

from app import app, db
from app.models import User, Employee, Bookproduct, Bookcategory, regulation
from functools import wraps
import json
import os
import hashlib


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username == username,
                             User.password == password).first()

def read_employees():
    employees = Employee.query.get(current_user.id)

    return employees


def read_bookcategories():
    bookcategories = Bookcategory.query.all()

    return bookcategories

def read_bookproducts(keyword=None):
    bookproducts = Bookproduct.query

    if keyword:
        bookproducts = bookproducts.filter(Bookproduct.name.contains(keyword))
    return bookproducts.all()

def add_bookproduct(name, quantity, price, image, bookcategory_id):
    bookproduct = Bookproduct(name=name,
                             quantity=quantity,
                             price=price,
                             image=image,
                             bookcategory_id=bookcategory_id)
    db.session.add(bookproduct)
    db.session.commit()

    return Bookproduct
def read_regulation(id, name, value):
    regulations = regulation.query.all()

    return  regulations



