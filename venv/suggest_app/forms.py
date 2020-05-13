from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms import SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange

AGE = {
    'min': 16, 'max': 85, 'message': 'Возраст должен быть от 16 до 85'
}
WEIGHT = {
    'min': 40, 'max': 150, 'message': 'Вес должен быть от 40 до 150 кг'
}
HEIGHT = {
    'min': 140, 'max': 210, 'message': 'Рост должен быть от 140 до 210 см'
}
WG = {
    'min': 9, 'max': 25, 'message': 'Обхват запястья должен быть от 9 до 25 см'
}
CG = {
    'min': 40, 'max': 160, 'message': 'Обхват груди должен быть от 40 до 160 см'
}


class CreateSuggest(FlaskForm):
    age = IntegerField(
        'Возраст', validators=[DataRequired(), NumberRange(**AGE)]
    )
    gender = SelectField(
        'Пол',
        choices=[
            ('m', 'Мужской'),
            ('f', 'Женский'),
        ],
        validators=[DataRequired()]
    )
    weight = FloatField(
        'Вес, кг', validators=[DataRequired(), NumberRange(**WEIGHT)]
    )
    height = FloatField(
        'Рост, см', validators=[DataRequired(), NumberRange(**HEIGHT)]
    )
    wg = FloatField(
        'Обхват запястья, см', validators=[DataRequired(), NumberRange(**WG)]
    )
    cg = FloatField(
        'Обхват груди, см', validators=[DataRequired(), NumberRange(**CG)]
    )
    real_calories = FloatField(
        'Калорий на неделю на данный момент, ккал', validators=[DataRequired()]
    )
    activity_level = SelectField(
        'Уровень повседневной активности',
        choices=[],
        validators=[DataRequired()]
    )
    eater_type = SelectField(
        'Тип питания',
        choices=[
            ('usual', 'Обычный'),
            ('vegan', 'Веганство'),
            ('vegat', 'Вегетарианство'),
            ('siroed', 'Сыроедение'),
        ],
        validators=[DataRequired()]
    )
    goal = SelectField(
        'Цель',
        choices=[],
        validators=[DataRequired()]
    )
    # period = SelectField(
    #     'Период',
    #     choices=[],
    #     validators=[DataRequired()]
    # )

    # body_type = SelectField(
    #     'Тип телосложения',
    #     choices=[
    #         ('1', 'Крупное'),
    #         ('2', 'Нормальное'),
    #         ('3', 'Худощавое'),
    #     ],
    #     validators=[DataRequired()]
    # )

    submit = SubmitField('Составить план')


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
