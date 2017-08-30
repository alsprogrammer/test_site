# coding: utf8

import os
from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, lm, oid
from forms import *
from models import *
from assessment_estimation.subjects import *

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
        group = Group(form.speciality.data, form.start_year.data, form.name.data)
        for student_name in form.students_list.data.splitlines():
            if student_name != u"\n":
                names = student_name.split(" ")
                if len(names) >= 3:
                    student = Student(names[0], names[1], names[2], group)
                elif len(names) == 2:
                    student = Student(names[0], first_name=names[1], group=group)
                elif len(names) == 1:
                    student = Student(names[0], group=group)
                else:
                    continue
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

