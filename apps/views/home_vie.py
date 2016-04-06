from flask import Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from apps.models import User
from flask import render_template, redirect, url_for, request
from apps.webservice import schedd, collector

myapp = Blueprint('myapp', __name__)


@myapp.route('/', methods=["GET"])
@myapp.route('/home', methods=["GET"])
def home():
    version = schedd.service.getVersionString()
    return render_template('home.html', version=version)


@myapp.route('/about', methods=["GET"])
def about():
    return render_template('about.html')


@myapp.route('/registe', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')


@myapp.route('/login', methods=["GET", "POST"])
def loginin():
    if current_user.is_authenticated:
        return redirect(url_for("myapp.home"))
    if request.method != 'POST':
        return render_template('login.html')

    uname = request.form["uname"]
    pwd = request.form["pwd"]
    rem = False
    if hasattr(request.form, "remember_me"):
        rem = True

    us = User.query.filter_by(user_name=uname).first()
    if us.check_pwd(pwd) and login_user(us, remember=rem):
        return redirect(url_for('myapp.home'))
    else:
        error = "登录名或密码错误"
        return render_template('login.html', error=error)

    # next = request.args.get('next')
    # # next_is_valid should check if the user has valid
    # # permission to access the `next` url
    # if not next_is_valid(next):
    #     return abort(400)


@myapp.route('/logout', methods=["GET", "POST"])
@login_required
def loginout():
    logout_user()
    return redirect(url_for("myapp.home"))

