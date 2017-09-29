from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
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
