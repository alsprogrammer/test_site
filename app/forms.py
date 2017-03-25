# coding: utf8

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class GroupForm(Form):
    speciality = StringField(u'Наименование специальности', validators=[DataRequired()])
    start_year = StringField(u'Год начала обучения', validators=[DataRequired()])
    name = StringField(u'Наименование группы', validators=[DataRequired()])
    students_list = TextAreaField()
