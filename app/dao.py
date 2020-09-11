
from app import app, db
from app.models import User, Employee, Bookproduct, Bookcategory
from functools import wraps
import json
import os
import hashlib


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username == username,
                             User.password == password).first()
def read_bookcategories():
    bookcategories = Bookcategory.query.all()

    return bookcategories.all()

def read_bookproducts():
    bookproducts = Bookproduct.query.all()

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



