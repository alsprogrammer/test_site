# coding: utf8

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, oid
from forms import *


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title=u"Добро пожаловать!")


@app.route('/admin/group/new', methods=['GET', 'POST'])
def admin_group_new():
    form = GroupForm()
    if form.validate_on_submit():
        flash(u"Группа добавлена")
        return redirect('/admin/group/list')
    return render_template("new_group.html", title=u"Добро пожаловать!", form=form)


@app.route('/test/start')
def test_start():
    return render_template("test.html", title=u"Добро пожаловать!")


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u"Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title=u"Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])

