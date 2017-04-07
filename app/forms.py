# coding: utf8

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
    speciality = StringField(u'Наименование специальности', validators=[DataRequired()])
    # The year the group has started to study
    start_year = StringField(u'Год начала обучения', validators=[DataRequired()])
    # The name of the goup
    name = StringField(u'Наименование группы', validators=[DataRequired()])
    # The list of students' names if form one student in one line, the sequence is Lastname Firstname Surname
    students_list = TextAreaField()
