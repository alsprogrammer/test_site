from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Form that appears when trying to get access to restricted part of the site"""
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class GroupForm(FlaskForm):
    """Form for entering the desciption of the new group"""
    # The name of the speciality the goup belongs to
    speciality = StringField('Наименование специальности', validators=[DataRequired("Название специальности является обязательным")])
    # The year the group has started to study
    start_year = StringField('Год начала обучения', validators=[DataRequired("Укажите год начала обучения")])
    # The name of the goup
    name = StringField('Наименование группы', validators=[DataRequired("Наименование группы является обязательным")])
    # The list of students' names if form one student in one line, the sequence is Lastname Firstname Surname
    students_list = TextAreaField(validators=[DataRequired("В группе должен быть хотя бы один студент")])


class StudentForm(FlaskForm):
    """Form for entering the desciption of a student"""
    # The name of the student
    first_name = StringField('Имя')
    # The surname of the student
    sur_name = StringField('Отчество')
    # The last name of the student
    last_name = StringField('Фамилия', validators=[DataRequired("Наличие фамилии является обязательным")])


class TestForm(FlaskForm):
    """Form for the loading of an assessment"""
    # The time for student to solve one task
    task_test_time = IntegerField('Время на один вопрос, сек', validators=[DataRequired('Необходимо указать время, даваемое на один вопрос')])
    # The number of tasks in an assessment
    task_num = IntegerField('Количество заданий в тесте', validators=[DataRequired('Необходимо задать количество заданий в тесте')])
    # The test file to download
    file = FileField('Файл с тестом')
