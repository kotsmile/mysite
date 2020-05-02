# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired
from suggest_app import app
from suggest_app import db
from flask import render_template
from suggest_app.forms import *

from flask import render_template, flash, redirect, url_for
from suggest_tool.models import *
from suggest_tool.calculator import get_menu, build_day_menu
from suggest_tool.paths import *

import pandas as pd

from flask_login import current_user, login_required, login_user, logout_user
from suggest_app.models import Admin


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(login=form.login.data).first()
        if admin is None or not admin.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(admin, remember=False)
        return redirect(url_for('admin'))
    return render_template('login.html', title='Войти в админ-панель', form=form)


@app.route('/admin')
def admin():
    if current_user.is_authenticated:
        return render_template('admin/panel.html', title='Админ-панель')

    return redirect(url_for('create_suggest'))



@app.route('/admin/activity_level', methods=['GET', 'POST'])
def admin_activity_level():
    if current_user.is_authenticated:

        activity_levels = load_pck(ACTIVITY_LEVELS_PATH)

        form = AddActivityLevel()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            activity = form.activity.data

            find = False
            for al in activity_levels:
                if al.abr == abr:
                    find = True
                    break
            if find:
                return redirect(url_for('admin_activity_level_add'))
            al = ActivityLevel(name=name, abr=abr, activity=activity)
            
            activity_levels.append(al)

            activity_levels = sorted(activity_levels, key=lambda x: x.activity)

            save_pck(activity_levels, ACTIVITY_LEVELS_PATH)

            return redirect(url_for('admin_activity_level'))

        return render_template(
            'admin/activity_level.html', 
            activity_levels=activity_levels, 
            title='Админ-панель',
            form=form
        )
    return redirect(url_for('create_suggest'))

@app.route('/admin/delete_activity_level/<abr>')
def delete_activity_level(abr):
    if current_user.is_authenticated:

        activity_levels = load_pck(ACTIVITY_LEVELS_PATH)

        new_activity_levels = []
        for al in activity_levels:
            if not al.abr == abr:
                new_activity_levels.append(al)

        new_activity_levels = sorted(new_activity_levels, key=lambda x: x.activity)

        save_pck(new_activity_levels, ACTIVITY_LEVELS_PATH)

        return redirect(url_for('admin_activity_level'))
    return redirect(url_for('create_suggest'))    



@app.route('/admin/goal', methods=['GET', 'POST'])
def admin_goal():
    if current_user.is_authenticated:

        goals = load_pck(GOALS_PATH)

        form = AddGoal()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            percent = form.percent.data / 100

            protein = form.protein.data / 100
            fat = form.fat.data / 100
            corb = form.corb.data / 100

            find = False
            for g in goals:
                if g.abr == abr:
                    find = True
                    break
            if find:
                return redirect(url_for('admin_goal'))
            g = Goal(name=name, abr=abr, percent=percent, pfc=[protein, fat, corb])
            

            goals.append(g)

            goals = sorted(goals, key=lambda x: x.percent)


            save_pck(goals, GOALS_PATH)

            return redirect(url_for('admin_goal'))

        return render_template(
            'admin/goal.html', 
            goals=goals, 
            title='Админ-панель', 
            form=form
        )

    return redirect(url_for('create_suggest'))

@app.route('/admin/delete_goal/<abr>')
def delete_goal(abr):
    if current_user.is_authenticated:

        goals = load_pck(GOALS_PATH)

        new_goals = []
        for g in goals:
            if not g.abr == abr:
                new_goals.append(g)

        new_goals = sorted(new_goals, key=lambda x: x.percent)

        save_pck(new_goals, GOALS_PATH)

        return redirect(url_for('admin_goal'))
    return redirect(url_for('create_suggest'))    



@app.route('/admin/period', methods=['GET', 'POST'])
def admin_period():
    if current_user.is_authenticated:

        periods = load_pck(PERIODS_PATH)

        form = AddPeriod()
        if form.validate_on_submit():
            name = form.name.data
            abr = form.abr.data
            days = form.days.data

            find = False
            for p in periods:
                if p.abr == abr:
                    find = True
                    break
            if find:
                return redirect(url_for('admin_period'))
            p = Period(name=name, abr=abr, days=days)
            

            periods.append(p)

            periods = sorted(periods, key=lambda x: x.days)


            pickle.save_pck(periods, PERIODS_PATH)
        
            return redirect(url_for('admin_period'))
        return render_template(
            'admin/period.html', 
            periods=periods, 
            title='Админ-панель',
            form=form,
        )

    return redirect(url_for('create_suggest'))

@app.route('/admin/delete_period/<abr>')
def delete_period(abr):
    if current_user.is_authenticated:

        periods = pickle.load_pck(PERIODS_PATH)
        new_periods = []
        for p in periods:
            if not p.abr == abr:
                new_periods.append(p)

        new_periods = sorted(new_periods, key=lambda x: x.days)

        save_pck(new_periods, PERIODS_PATH)
        return redirect(url_for('admin_period'))

    return redirect(url_for('create_suggest'))    



@app.route('/admin/recipes', methods=['GET', 'POST'])
def admin_recipes():
    if current_user.is_authenticated:

        recipes = load_pck(RECIPES_PATH)

        form = AddRecipe()
        if form.validate_on_submit():
            link = form.link.data
            recipe_types = form.recipe_type.data

            new_r = Recipe(link=link, recipe_type=d_recipe_types[recipe_types[0]])
            all_r = [Recipe(link=link, recipe_type=d_recipe_types[r]) for r in recipe_types]

            find = False
            for r in recipes:
                if r.code == new_r.code and r.recipe_type.abr in recipe_types:
                    find = True
                    break
            if find:
                return redirect(url_for('admin_recipes'))

            recipes += all_r
            recipes = sorted(recipes, key=lambda x: x.name)

            save_pck(recipes, RECIPES_PATH)

            return redirect(url_for('admin_recipes'))

        up_conv = {
            0: ('Не обновлено', 'red'),
            1: ('Обновляется...', 'gray'),
            2: ('Обновлено', 'green')
        }
        return render_template(
            'admin/recipes.html', 
            recipes=recipes,
            update=up_conv[load_pck(UPDATE_PATH)][0],
            color=up_conv[load_pck(UPDATE_PATH)][1],
            title='Админ-панель',
            form=form
        )

    return redirect(url_for('create_suggest'))

@app.route('/admin/delete_recipes/<q>')
def delete_recipes(q):
    code, abr = int(q.split('&')[0]), q.split('&')[1]
    if current_user.is_authenticated:

        recipes = load_pck(RECIPES_PATH)

        new_recipes = []
        for r in recipes:
            if not (r.code == code and r.recipe_type.abr == abr):
                new_recipes.append(r)

        new_recipes = sorted(new_recipes, key=lambda x: x.name)

        save_pck(new_recipes, RECIPES_PATH)

        day_menu = pd.read_pickle(DAY_MENU_PATH)

        day_menu = day_menu[day_menu['Завтрак'] != int(code)]
        day_menu = day_menu[day_menu['Обед'] != int(code)]
        day_menu = day_menu[day_menu['Перекус'] != int(code)]
        day_menu = day_menu[day_menu['Ужин'] != int(code)]

        day_menu.to_pickle(DAY_MENU_PATH)

        return redirect(url_for('admin_recipes'))

    return redirect(url_for('create_suggest'))    

@app.route('/admin/recipes_update')
def admin_recipes_update():
    if current_user.is_authenticated:

        if load_pck(UPDATE_PATH) in [1, 2]:
            return redirect(url_for('admin_recipes'))

        build_day_menu()
        
        
        return redirect(url_for('admin_recipes'))
        
    return redirect(url_for('create_suggest'))  



@app.route('/admin/eq_conf', methods=['GET', 'POST'])
def admin_eq_conf():
    if current_user.is_authenticated:

        eq_conf = load_pck(EQ_CONF_PATH)

        form = EditEqConf()
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


            save_pck(new_eq_conf, EQ_CONF_PATH)

            return redirect(url_for('admin_eq_conf'))

        return render_template(
            'admin/eq_conf.html', 
            eq_conf=eq_conf, 
            title='Админ-панель',
            form=form
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
    code_recipes = load_pck(CODE_RECIPES_PATH)
    recipe = code_recipes[code]
    

    return render_template('recipe.html', title='Рецепт', recipe=recipe)


@app.route('/', methods=['GET', 'POST'])
def create_suggest():

    class CreateSuggest(FlaskForm):
        age = IntegerField('Возраст', validators=[DataRequired()])
        weight = FloatField('Вес, кг', validators=[DataRequired()])
        height = FloatField('Рост, см', validators=[DataRequired()])

        fat_percent = FloatField('Процент жиров, %', validators=[DataRequired()])


        activity_levels = load_pck(ACTIVITY_LEVELS_PATH)
        goals = load_pck(GOALS_PATH)
        periods = load_pck(PERIODS_PATH)

        activity_levels_choices = [(al.abr, al.name) for al in activity_levels]
        goals_choices = [(g.abr, g.name) for g in goals]
        periods_choices = [(p.abr, p.name) for p in periods]

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
            str(form.fat_percent.data),
            str(form.activity_level.data),
            str(form.goal.data),
            str(form.period.data),
        ]
        quary = '&'.join(quaries)
        return redirect(f'/menu/' + quary)

    return render_template('enter_user_data.html', title='Данные пользователя', form=form)


@app.route('/menu/<quary>')
def menu(quary):
    age, weight, height, fat_percent, activity_level_abr, goal_abr, period_abr = quary.split('&')

    age = int(age)
    weight = float(weight)
    height = float(height)
    fat_percent = float(fat_percent)

    users = load_pck(USERS_PATH)

    new_id = users[-1].id_ + 1

    user = User(
        id_=new_id,
        age=age,
        weight=weight,
        height=height,
        fat_percent=fat_percent,
        activity_level=activity_level_abr,
        goal=goal_abr,
        period=period_abr
    )

    users.append(user)
    save_pck(users, USERS_PATH)
    ans = get_menu(user)
    if ans == -1:
        return 'Не можем подобрать для вас меню :('
    days, calories, protein, fat, corb = ans
    
    return render_template(
        'menu.html', 
        title='Меню', 
        days=days,
        calories=int(calories),
        protein=int(protein),
        fat=int(fat),
        corb=int(corb)
    )
            
