from flask import render_template, flash, redirect, session, url_for, request, g
from werkzeug.utils import secure_filename
from app import app, lm, oid, groups_to_test, tasksets, passing, passed, ready_to_test
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
        return redirect(url_for('group_edit', group_uid=group_uid))

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
    return render_template("test_list.html", tests=tasksets)


@app.route('/test/admin/test/allow', methods=['GET', 'POST'])
def allow_to_test():
    """Allows students to pass an assessment"""
    form = AllowTestForm()
    form.assessment.choices = [(cur_assessment, tasksets[cur_assessment].name) for cur_assessment in tasksets]
    students = []
    for cur_group in groups_to_test:
        for cur_student in groups_to_test[cur_group].students:
            students.append((cur_group + '.' + cur_student, groups_to_test[cur_group].students[cur_student].__repr__()))
    form.students.choices = students
    if form.validate_on_submit():
        if form.assessment.data not in tasksets.keys():
            flash("Нет такого теста")
            return redirect(url_for('test_list'))

        taskset = tasksets[form.assessment.data]

        for cur_student in form.students.data:
            student_data = cur_student.split('.')
            group_uuid = student_data[0]
            student_uuid = student_data[1]
            if group_uuid not in groups_to_test.keys():
                flash("Нет такой группы")
                return redirect(url_for('group_list'))

            if student_uuid not in groups_to_test[student_data[0]].students.keys():
                flash("Нет такого студента")
                return redirect(url_for('test_list'))

            assessment = taskset.create_test(taskset.tasks_num, student=groups_to_test[group_uuid].students[student_uuid])
            ready_to_test.update({uuid.uuid4().hex: assessment})

        return redirect(url_for('test_passing'))

    return render_template("test_allow.html", title="Добро пожаловать!", form=form)


@app.route('/test/admin/passing')
def test_passing():
    """Show the test system description page before test starts"""
    return render_template("test_passing.html", passing=passing)


@app.route('/test/start')
def test_start():
    """Show the test system description page before test starts"""
    return render_template("test.html", title="Добро пожаловать!", list=ready_to_test)


@app.route('/test/pass/<assessment_uuid>', methods=['GET', 'POST'])
def test_pass(assessment_uuid):
    """Show the test system description page before test starts"""
    if request.method == 'GET':
        if assessment_uuid not in ready_to_test.keys():
            flash("Нет такого теста")
            return redirect(url_for('allow_to_test'))

        cur_assessment = ready_to_test[assessment_uuid]
        cur_assessment.started = datetime.datetime.now()
        del ready_to_test[assessment_uuid]
        passing.update({assessment_uuid: cur_assessment})

        return render_template("test_site.html", title="Добро пожаловать!", assessment_uid=assessment_uuid, assessment=cur_assessment)

    elif request.method == 'POST':
        if assessment_uuid not in passing.keys():
            flash("Нет такого теста")
            return redirect(url_for('allow_to_test'))

        assessment = passing[assessment_uuid]
        assessment.ended = datetime.datetime.now()
        results = request.form

        assessment.get_score(set(results))

        del passing[assessment_uuid]
        passed.update({assessment_uuid: assessment})

        with open(os.path.join(app.config["DATA_PATH"], assessment_uuid + '.rjsn'), 'w', encoding='utf-8') as result_file:
            res_descr = json.dumps(assessment.to_dict(), ensure_ascii=False)
            result_file.write(res_descr)
            result_file.flush()
        return redirect(url_for('show_result', assessment_uid=assessment_uuid))


@app.route('/test/showresult/<assessment_uid>')
def show_result(assessment_uid):
    """Show the result of the test"""
    if assessment_uid not in passed.keys():
        flash("Нет такого теста")
        return redirect(url_for('index'))

    assessment = passed[assessment_uid]
    return render_template("result.html", assessment=assessment)


@app.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Вы запросили вход для " + form.openid.data)
        return redirect('/index')

    return render_template("login.html", title="Вход в систему", form=form, providers=app.config['OPENID_PROVIDERS'])
