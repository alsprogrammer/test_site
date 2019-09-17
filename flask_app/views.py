from flask import render_template, flash, redirect, session, url_for, request, g
from werkzeug.utils import secure_filename
from app import app, lm, oid, groups_to_test, passing, passed, ready_to_test
from .forms import *
from assessment_estimation.models import *
import uuid
import json
import os

from app import assessment_service


@app.route('/test')
@app.route('/test/start')
def test_start():
    """Show the test system description page before test starts"""

    result = render_template("test.html", title="Добро пожаловать!",
                             list=sorted(ready_to_test.items(), key=lambda pair: pair[1].student.__repr__()))

    return result


@app.route('/test/admin')
@app.route('/test/admin/statistics')
def statistics():
    """Show the test system description page before test starts"""
    return render_template("statistics.html", passed=passed,
                           passed_keys=sorted(passed, key=lambda passed_key:passed[passed_key].ended))


@app.route('/test/showresult/<assessment_uid>')
def show_result(assessment_uid):
    """Show the result of the test"""
    if assessment_uid not in passed.keys():
        flash("Нет такого теста")
        return redirect(url_for('index'))

    return render_template("result.html", assessment=passed[assessment_uid])


@app.route('/test/admin/passing_delete/<passing_uid>')
def passing_delete(passing_uid):
    if passing_uid not in passing.keys():
        flash("Нет такого тестируемого")
        return redirect(url_for('test_passing'))

    assessment_service.cancel_assessment(passing_uid)
    return redirect(url_for('test_passing'))


@app.route('/test/admin/allowed_delete/<assessment_uuid>')
def allowed_delete(assessment_uuid):
    if assessment_uuid not in ready_to_test.keys():
        flash("Нет такого допущенного")
        return redirect(url_for('test_passing'))

    assessment_service.remove_assessment(assessment_uuid)
    return redirect(url_for('test_allowed'))


@app.route('/test/admin/group/list')
def group_list():
    """Show the test system description page before test starts"""
    return render_template("group_list.html", groups=groups_to_test,
                           groups_keys=sorted(groups_to_test, key=lambda group_key: groups_to_test[group_key].name))


@app.route('/test/admin/passing')
def test_passing():
    """Show the test system description page before test starts"""
    return render_template("test_passing.html", passing=passing)


@app.route('/test/admin/allowed')
def test_allowed():
    """Show the test system description page before test starts"""
    return render_template("test_allowed.html", title="Добро пожаловать!",
                           list=sorted(ready_to_test.items(), key=lambda pair: pair[1].student.__repr__()))


@app.route('/test/pass/<assessment_uuid>', methods=['GET', 'POST'])
def test_pass(assessment_uuid):
    """Show the test system description page before test starts"""
    if assessment_uuid not in ready_to_test.keys():
        flash("Нет такого теста")
        return redirect(url_for('test_start'))

    if request.method == 'GET':
        cur_assessment = assessment_service.start_assessment(assessment_uuid)

        return render_template("test_site.html", title="Добро пожаловать!",
                               assessment_uid=assessment_uuid, assessment=cur_assessment)

    elif request.method == 'POST':
        results = request.form
        assessment_service.answer_assessment(assessment_uuid, results)

        return redirect(url_for('show_result', assessment_uid=assessment_uuid))


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title="Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])


############
# The rest here are methods to re-implement
############
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
                    names = student_name.strip().split(" ")
                    if len(names) >= 3:
                        student = Student(last_name=names[0], first_name=names[1], sur_name=names[2], group=group)
                    elif len(names) == 2:
                        student = Student(last_name=names[0], first_name=names[1], group=group)
                    elif len(names) == 1:
                        student = Student(last_name=names[0], group=group)
                    else:
                        continue

                    group.add_student(student)

            uu = uuid.uuid4().hex
            groups_to_test.update({uu: group})
            group_descr = json.dumps(group.to_dict(), ensure_ascii=False)
            group_file = open(os.path.join(app.config["DATA_PATH"], uu+".gjsn"), mode="w", encoding='utf-8')
            group_file.write(group_descr)
            group_file.flush()
            group_file.close()

            flash("Группа добавлена")
            return redirect('/test/admin/group/list')

    if err_message:
        flash(err_message)
    return render_template("new_group.html", title="Добро пожаловать!", form=form)


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
        return redirect(url_for('group_edit', group_uid=group_uid))

    group = groups_to_test[group_uid]
    student = group.students[student_uid]
    form = StudentForm(first_name=student.first_name, sur_name=student.sur_name, last_name=student.last_name)
    if form.validate_on_submit():
        groups_to_test[group_uid].students[student_uid].last_name = form.last_name.data
        groups_to_test[group_uid].students[student_uid].first_name = form.first_name.data
        groups_to_test[group_uid].students[student_uid].sur_name = form.sur_name.data

        group_descr = json.dumps(groups_to_test[group_uid].to_dict(), ensure_ascii=False)
        group_file = open(os.path.join(app.config["DATA_PATH"], group_uid + ".gjsn"), mode="w+", encoding='utf-8')
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
    form = TestForm()
    if form.validate_on_submit():
        # check if the post request has the file part
        filename = os.path.join(app.config["DATA_PATH"], secure_filename(form.file.data.filename))
        form.file.data.save(filename)

        testset = TasksPool(assessment_desciption=filename)
        testset.time_per_task = form.task_test_time.data
        testset.tasks_num = form.task_num.data
        uid = uuid.uuid4().hex
        tasksets.update({uid: testset})

        with open(os.path.join(app.config["DATA_PATH"], uid + '.tjsn'), 'w', encoding='utf-8') as tasksetfile:
            test_descr = json.dumps(testset.to_dict(), ensure_ascii=False)
            tasksetfile.write(test_descr)
            tasksetfile.flush()

        os.remove(filename)

        return redirect(url_for('test_list'))

    return render_template("test_new.html", title="Добро пожаловать!", form=form)


@app.route('/test/admin/test/list')
def test_list():
    """Show the test system description page before test starts"""
    return render_template("test_list.html", tests=tasksets,
                           test_keys=sorted(tasksets, key=lambda test_key: tasksets[test_key].name))
