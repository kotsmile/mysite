from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from suggest_app.models import User


class CreateSuggest(FlaskForm):
    age = IntegerField('Возраст', validators=[DataRequired()])
    weight = FloatField('Вес, кг', validators=[DataRequired()])
    height = FloatField('Рост, см', validators=[DataRequired()])

    gender = SelectField(
        'Пол',
        choices=[
            ('m', 'Мужской'),
            ('f', 'Женский'),
        ],
        validators=[DataRequired()]
    )

    body_type = SelectField(
        'Тип телосложения',
        choices=[
            ('1', 'Крупное'),
            ('2', 'Нормальное'),
            ('3', 'Худощавое'),
        ],
        validators=[DataRequired()]
    )
    activity_level = SelectField(
        'Уровень повседневной активности',
        choices=[],
        validators=[DataRequired()]
    )
    goal = SelectField(
        'Цель',
        choices=[],
        validators=[DataRequired()]
    )
    period = SelectField(
        'Период',
        choices=[],
        validators=[DataRequired()]
    )
    submit = SubmitField('Составить меню')



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


# field = name, label, type
