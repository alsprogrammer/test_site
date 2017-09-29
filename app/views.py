from flask import render_template, flash, redirect, session, url_for, request, g
from werkzeug.utils import secure_filename
from app import app, lm, oid, groups_to_test
from .forms import *
from assessment_estimation.subjects import *
import uuid
import json
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/test')
def index():
    """Show the first page of the testing system."""
    return render_template("index.html", title="Добро пожаловать!")


@app.route('/test/admin/group/new', methods=['GET', 'POST'])
def group_new():
    """Add new group to the testing system.
    The group json file will be saved to the folder specified in config
    """
    err_message = ""
    form = GroupForm()
    if form.validate_on_submit():
        found = False
        for group_uid in groups_to_test:
            if groups_to_test[group_uid].name == form.name.data:
                found = True
                err_message = "Такая группа уже существует"
                break
        if not found:
            group = Group(form.speciality.data, form.start_year.data, form.name.data)
            for student_name in form.students_list.data.splitlines():
                if student_name != "\n":
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

            uu = uuid.uuid4().hex
            groups_to_test.update({uu: group})
            group_descr = json.dumps(group.to_dict(), ensure_ascii=False)
            group_file = open(os.path.join(app.config["DATA_PATH"], uu+".gjsn"), mode="w")
            group_file.write(group_descr)
            group_file.flush()
            group_file.close()

            flash("Группа добавлена")
            return redirect('/test/admin/group/list')

    if err_message:
        flash(err_message)
    return render_template("new_group.html", title="Добро пожаловать!", form=form)


@app.route('/test/admin/group/list')
def group_list():
    """Show the test system description page before test starts"""
    return render_template("group_list.html", groups=groups_to_test)


@app.route('/test/admin/group/edit/<group_uid>')
def group_edit(group_uid):
    """Show the test system description page before test starts"""
    if group_uid not in groups_to_test.keys():
        flash("Такой группы не существует")
        return redirect(url_for('group_list'))

    return render_template("group_edit.html", group_uid=group_uid, group=groups_to_test[group_uid])


@app.route('/test/admin/student/edit/<group_uid>/<student_uid>', methods=['GET', 'POST'])
def student_edit(group_uid, student_uid):
    """Edit the given student"""
    if group_uid not in groups_to_test.keys():
        flash("Такой группы не существует")
        return redirect(url_for('group_list'))

    if student_uid not in groups_to_test[group_uid].students.keys():
        flash("Такого студента не существует")
        return redirect(url_for('group_list'))

    group = groups_to_test[group_uid]
    student = group.students[student_uid]
    form = StudentForm(first_name=student.first_name, sur_name=student.sur_name, last_name=student.last_name)
    if form.validate_on_submit():
        groups_to_test[group_uid].students[student_uid].last_name = form.last_name.data
        groups_to_test[group_uid].students[student_uid].first_name = form.first_name.data
        groups_to_test[group_uid].students[student_uid].sur_name = form.sur_name.data

        group_descr = json.dumps(groups_to_test[group_uid].to_dict(), ensure_ascii=False)
        group_file = open(os.path.join(app.config["DATA_PATH"], group_uid + ".gjsn"), mode="w+")
        group_file.write(group_descr)
        group_file.flush()
        group_file.close()

        flash("Студент изменен")
        return redirect(url_for('group_edit', group_uid=group_uid))

    return render_template("student_edit.html", title="Добро пожаловать!", form=form)


@app.route('/test/admin/test/new', methods=['GET', 'POST'])
def test_new():
    """Add new group to the testing system.
    The group json file will be saved to the folder specified in config
    """
    err_message = ""
    form = GroupForm()
    if form.validate_on_submit():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route('/test/start')
def test_start():
    """Show the test system description page before test starts"""
    return render_template("test.html", title="Добро пожаловать!")


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title="Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])
