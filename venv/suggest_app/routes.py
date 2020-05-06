# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired

from flask import render_template, redirect, url_for

from flask_login import current_user, login_user, logout_user

from suggest_app import app

from suggest_app.models import Admin
import suggest_app.forms as forms

from suggest_tool.calculator import get_menu
import suggest_tool.models_tool as mtool
import suggest_tool.models as stmodels


EXIST_ERROR = 'Уже существует'
NONE_ERROR = ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = forms.LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(login=form.login.data).first()
        if admin is None or not admin.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(admin, remember=False)
        return redirect(url_for('admin'))
    return render_template(
        'login.html',
        title='Войти в админ-панель',
        form=form,
    )


@app.route('/admin')
def admin():
    if current_user.is_authenticated:
        return render_template('admin/panel.html', title='Админ-панель')

    return redirect(url_for('create_suggest'))


@app.route('/admin/activity_level', methods=['GET', 'POST'])
def admin_activity_level():
    if current_user.is_authenticated:

        form = forms.AddActivityLevel()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            activity = form.activity.data
            new_activity_level = stmodels.ActivityLevel(
                name=name,
                abr=abr,
                activity=activity
            )

            if mtool.add_activity_level(new_activity_level):
                error = NONE_ERROR
            else:
                error = EXIST_ERROR

            return render_template(
                'admin/activity_level.html',
                activity_levels=sorted(
                    mtool.get_activity_levels(),
                    key=lambda x: x.activity
                ),
                title='Админ-панель',
                form=form,
                error=error
            )

        return render_template(
            'admin/activity_level.html',
            activity_levels=sorted(
                mtool.get_activity_levels(),
                key=lambda x: x.activity
            ),
            title='Админ-панель',
            form=form,
        )

    return redirect(url_for('create_suggest'))


@app.route('/admin/delete_activity_level/<abr>')
def delete_activity_level(abr):
    if current_user.is_authenticated:

        mtool.remove_activity_level(abr)
        return redirect(url_for('admin_activity_level'))

    return redirect(url_for('create_suggest'))


@app.route('/admin/goal', methods=['GET', 'POST'])
def admin_goal():

    if current_user.is_authenticated:

        form = forms.AddGoal()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            percent = form.percent.data / 100

            protein = form.protein.data / 100
            fat = form.fat.data / 100
            corb = form.corb.data / 100

            breakfast = form.breakfast.data / 100
            lunch = form.lunch.data / 100
            dinner = form.dinner.data / 100

            new_goal = stmodels.Goal(
                name=name,
                abr=abr,
                percent=percent,
                pfc=[protein, fat, corb],
                breakfast=breakfast,
                lunch=lunch,
                dinner=dinner
            )

            if mtool.add_goal(new_goal):
                error = NONE_ERROR
            else:
                error = EXIST_ERROR

            return render_template(
                'admin/goal.html',
                goals=sorted(mtool.get_goals(), key=lambda x: x.percent),
                title='Админ-панель',
                form=form,
                error=error
            )

        return render_template(
            'admin/goal.html',
            goals=sorted(mtool.get_goals(), key=lambda x: x.percent),
            title='Админ-панель',
            form=form,
        )

    return redirect(url_for('create_suggest'))


@app.route('/admin/delete_goal/<abr>')
def delete_goal(abr):
    if current_user.is_authenticated:

        mtool.remove_goal(abr)
        return redirect(url_for('admin_goal'))

    return redirect(url_for('create_suggest'))


@app.route('/admin/period', methods=['GET', 'POST'])
def admin_period():
    if current_user.is_authenticated:
        error = NONE_ERROR
        form = forms.AddPeriod()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            days = form.days.data

            new_period = stmodels.Period(name=name, abr=abr, days=days)

            if not mtool.add_period(new_period):
                error = EXIST_ERROR

        return render_template(
            'admin/period.html',
            periods=sorted(mtool.get_periods(), key=lambda x: x.days),
            title='Админ-панель',
            form=form,
            error=error
        )

    return redirect(url_for('create_suggest'))


@app.route('/admin/delete_period/<abr>')
def delete_period(abr):
    if current_user.is_authenticated:

        mtool.remove_period(abr)
        return redirect(url_for('admin_period'))

    return redirect(url_for('create_suggest'))


@app.route('/admin/recipes', methods=['GET', 'POST'])
def admin_recipes():
    if current_user.is_authenticated:

        form = forms.AddRecipe()
        if form.validate_on_submit():
            link = form.link.data
            rt = form.recipe_type.data

            new_recipe = stmodels.Recipe(
                link=link,
                recipe_type=stmodels.abr_to_recipe_typed_recipe_types[rt]
            )

            if mtool.add_recipe(new_recipe):
                error = NONE_ERROR
            else:
                error = EXIST_ERROR

            return render_template(
                'admin/recipes.html',
                recipes=sorted(mtool.get_recipes(), key=lambda x: x.code),
                title='Админ-панель',
                form=form,
                error=error
            )

        return render_template(
            'admin/recipes.html',
            recipes=sorted(mtool.get_recipes(), key=lambda x: x.code),
            title='Админ-панель',
            form=form,
        )

    return redirect(url_for('create_suggest'))


@app.route('/admin/delete_recipes/<code>')
def delete_recipes(code):
    code = int(code)
    if current_user.is_authenticated:

        mtool.remove_recipe(code)
        return redirect(url_for('admin_recipes'))

    return redirect(url_for('create_suggest'))


@app.route('/admin/eq_conf/<gender>', methods=['GET', 'POST'])
def admin_eq_conf(gender):
    if current_user.is_authenticated:

        eq_conf = mtool.get_eq_conf(gender)

        form = forms.EditEqConf()
        if form.validate_on_submit():
            const = form.const.data
            c_weight = form.c_weight.data
            c_height = form.c_height.data
            c_age = form.c_age.data

            new_eq_conf = {
                'const': const,
                'c_weight': c_weight,
                'c_height': c_height,
                'c_age': c_age,
            }

            mtool.set_eq_conf(new_eq_conf, gender)
            return redirect(url_for('admin_eq_conf'))

        return render_template(
            'admin/eq_conf.html',
            eq_conf=eq_conf,
            title='Админ-панель',
            form=form,
        )

    return redirect(url_for('create_suggest'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('create_suggest'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('create_suggest'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         admin = Admin(login=form.login.data)
#         admin.set_password(form.password.data)
#         db.session.add(admin)
#         db.session.commit()

#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


@app.route('/recipe/<code>')
def recipe(code):
    code = int(code)
    recipe = mtool.get_recipe(code)

    return render_template('recipe.html', title='Рецепт', recipe=recipe)


@app.route('/', methods=['GET', 'POST'])
def create_suggest():

    class CreateSuggest(FlaskForm):
        age = IntegerField('Возраст', validators=[DataRequired()])
        weight = FloatField('Вес, кг', validators=[DataRequired()])
        height = FloatField('Рост, см', validators=[DataRequired()])

        activity_levels = mtool.get_activity_levels()
        goals = mtool.get_goals()
        periods = mtool.get_periods()

        activity_levels_choices = [(al.abr, al.name) for al in activity_levels]
        goals_choices = [(g.abr, g.name) for g in goals]
        periods_choices = [(p.abr, p.name) for p in periods]

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
            choices=activity_levels_choices,
            validators=[DataRequired()]
        )
        goal = SelectField(
            'Цель',
            choices=goals_choices,
            validators=[DataRequired()]
        )
        period = SelectField(
            'Период',
            choices=periods_choices,
            validators=[DataRequired()]
        )

        submit = SubmitField('Составить меню')
    form = CreateSuggest()
    if form.validate_on_submit():

        quaries = [
            str(form.age.data),
            str(form.weight.data),
            str(form.height.data),
            str(form.gender.data),
            str(form.activity_level.data),
            str(form.goal.data),
            str(form.period.data),
        ]
        quary = '&'.join(quaries)
        return redirect(f'/menu/' + quary)

    return render_template(
        'enter_user_data.html',
        title='Данные пользователя',
        form=form
    )


@app.route('/menu/<quary>')
def menu(quary):
    print(quary)
    age, weight, height, gender, activity_level_abr, goal_abr, period_abr = quary.split('&')

    age = int(age)
    weight = float(weight)
    height = float(height)

    user = stmodels.User(
        age=age,
        weight=weight,
        height=height,
        gender=gender,
        activity_level=activity_level_abr,
        goal=goal_abr,
        period=period_abr
    )
    mtool.add_user(user)

    ans = get_menu(user)
    if ans == -1:
        return 'Не можем подобрать для вас меню :('
    days, calories, protein, fat, corb = ans

    return render_template(
        'menu.html',
        title='Меню',
        days=days,
        calories=calories,
        protein=protein,
        fat=fat,
        corb=corb
    )
