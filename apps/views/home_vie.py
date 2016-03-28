from flask import Flask, Blueprint
from flask.ext.login import login_user, logout_user, current_user, login_required
from apps.models import User
from flask import render_template, flash, redirect, session, url_for, request, g
from apps.webservice import schedd, collector

myapp = Blueprint('myapp', __name__)


@myapp.route('/')
@myapp.route('/home')
def home():
    version=schedd.service.getVersionString()
    return render_template('home.html', version=version)


@myapp.route('/about')
def about():
    return '这是关于'


@myapp.route('/login', methods=["GET", "POST"])
def loginin():
    if current_user.is_authenticated:
        return redirect(url_for("myapp.home"))
    if request.method != 'POST':
        return render_template('login.html')

    # session['remember_me'] = request.form.get('remember_me')
    uname = request.form["uname"]
    pwd = request.form["pwd"]
    # if request.form.getattribute("remember_me"):
    #     session['remember_me'] = request.form['remember_me']

    us = User.query.filter_by(user_name=uname).first()
    if us.check_pwd(pwd) and login_user(us):
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

