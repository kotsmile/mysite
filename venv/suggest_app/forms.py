from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, PasswordField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from suggest_app.models import Admin

import pickle
from suggest_tool.paths import *
from suggest_tool.models import recipe_types

class AddActivityLevel(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    abr = StringField('Аббравиатура', validators=[DataRequired()])
    activity = FloatField('Уровень', validators=[DataRequired()])

    submit = SubmitField('Добавить')

class AddRecipe(FlaskForm):
    link = StringField('Ссылка (edimdoma / eda)', validators=[DataRequired()])
    recipe_type_choices = [(rt.abr, rt.name) for rt in recipe_types]

    recipe_type = SelectField(
        'Прием пищи',
        choices=recipe_type_choices, 
        validators=[DataRequired()]
    )

    submit = SubmitField('Добавить')

class EditEqConf(FlaskForm):
    const = FloatField('const', validators=[DataRequired()])
    c_weight = FloatField('c_weight', validators=[DataRequired()])
    c_height = FloatField('c_height', validators=[DataRequired()])
    c_age = FloatField('c_age', validators=[DataRequired()])

    submit = SubmitField('Изменить')

class AddGoal(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    abr = StringField('Аббравиатура', validators=[DataRequired()])
    percent = FloatField('Процент от нормы, %', validators=[DataRequired()])

    protein = FloatField('Процент белков, %', validators=[DataRequired()])
    fat = FloatField('Процент жиров, %', validators=[DataRequired()])
    corb = FloatField('Процент углеводов, %', validators=[DataRequired()])

    breakfast = FloatField('Процент КБЖУ на завтрак, %', validators=[DataRequired()])
    lunch = FloatField('Процент КБЖУ на обед, %', validators=[DataRequired()])
    dinner = FloatField('Процент КБЖУ на ужин, %', validators=[DataRequired()])

    submit = SubmitField('Добавить')

class AddPeriod(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    abr = StringField('Аббравиатура', validators=[DataRequired()])
    days = IntegerField('Количество дней', validators=[DataRequired()])

    submit = SubmitField('Добавить')




class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
   
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        admin = Admin.query.filter_by(login=login.data).first()
        if admin is not None:
            raise ValidationError('Please use a different username.')
