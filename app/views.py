# coding: utf8

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, oid
from forms import LoginForm
#from models import User, ROLE_USER, ROLE_ADMIN
import clr
clr.AddReference("TestClass")
from TestClass import TestImage, Student, Group, WholeTest, Test, StudentTestAnswer


@app.route('/')
@app.route('/index')
def index():
    test = WholeTest("f:\\Test\\ttt.xml")
    return "Hello, world!"#render_template("index.html", title=u"Добро пожаловать!", user=user, posts=posts)


@app.route('/login/',  methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u"Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title=u"Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])

