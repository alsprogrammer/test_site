# coding: utf8

import os
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, oid
from forms import *
from bs4 import BeautifulSoup
from config import DATA_PATH
from models import *

@app.route('/')
@app.route('/index')
def index():
    """Show the first page of the testing system."""
    return render_template("index.html", title=u"Добро пожаловать!")


@app.route('/admin/group/new', methods=['GET', 'POST'])
def admin_group_new():
    """Add new group to the testing system.
    The group xml file will be saved to the ... folder
    """
    form = GroupForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            group = Group(form.speciality.data, form.start_year.data, form.name.data)
            for student_name in form.students_list.data.splitlines():
                names = student_name.split()
                student = Student(names[0], names[1], names[2], group)
                group.add_student(student)
                group.save_to_xml_file(os.path.join(DATA_PATH, "group.xml"))

            flash(u"Группа добавлена")
            return redirect('/admin/group/list')

    return render_template("new_group.html", title=u"Добро пожаловать!", form=form)


@app.route('/test/start')
def test_start():
    """Show the test system description page before test starts"""
    return render_template("test.html", title=u"Добро пожаловать!")


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u"Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title=u"Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])

