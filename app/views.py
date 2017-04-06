# coding: utf8

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, oid
from forms import *


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
        source_xml = '<?xml version="1.0" encoding="utf-8" standalone="yes"?><group></group>'
        if request.method == 'POST':
            source_xml.group.speciality
            for student_name in form.students_list:
                names = student_name.split()

            values = {'first_name': form.first_name.data,
                      'age': form.age.data,
                      'gender': form.gender.data,
                      'search_gender': form.search_gender.data}
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

