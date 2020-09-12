from werkzeug.utils import redirect
from flask_login import login_user
from app import app, login, dao, decorator
from flask import render_template, request, url_for

from app.decorator import login_required
from app.models import *
import hashlib


@app.route("/")
def index():
   return render_template("login-nv.html")


@app.route("/home", methods=["get", "post"])
def signin_user():
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.check_login(username=username, password=password)
        if user:
            if user.staff_role == "WAREHOUSE":
                return render_template("infostaff.html")
            if user.staff_role == "CASHIER":
                return  render_template("home.html")
            login_user(user=user)
        else:
            return  render_template("login-nv.html")
    return render_template("login-nv.html", err_msg=err_msg)


@app.route("/infostaff")
@decorator.login_required
def info_staff():
    employees=dao.read_employees()
    import pdb
    pdb.set_trace()
    return render_template("inforstaff.html", employees=employees)


@app.route("/home")
def home_us():
    return render_template("home.html")

@app.route("/booklist-sale", methods=["GET", "POST"])
def booklist_cashier():
    kw = request.args.get("keyword")
    return render_template("book-list.html", bookproducts=dao.read_bookproducts(keyword=kw))

@app.route("/infostaff/add", methods=["GET","POST"])
def add_or_update_bookproduct():
    if request.method == "POST":
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        price = request.form.get("price", 0)
        bookcategory_id = request.form.get("bookcategory_id")

        if dao.add_bookproduct(name=name, quantity=quantity, price=price, image="", bookcategory_id=bookcategory_id):
            return redirect(url_for("info_staff"))
    return render_template("bookproduct-add.html", Bookcategory=dao.read_bookcategories())


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                          User.password == password).first()
        if user:
            login_user(user=user)
    return redirect("/admin")


@login.user_loader
def user_loaf(user_id):
    return  User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True, port=5555)