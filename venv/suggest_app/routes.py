# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for

from flask_login import current_user, login_user, logout_user

from suggest_app import app, db

from suggest_app.models import User, ActivityLevel, Period, Goal, Item, Category
import suggest_app.forms as forms
from suggest_app.forms import RegistrationForm

from suggest_tool.calculator import get_menu
import suggest_tool.models as stmodels

import pickle
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin')

    form = forms.LoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(login=form.login.data).first()
        if admin is None or not admin.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(admin, remember=False)
        return redirect('/admin')
    return render_template(
        'login.html',
        title='Войти в админ-панель',
        form=form,
    )

@app.route('/add_group', methods=['GET', 'POST'])
def add_to_group():
    pass

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('create_suggest'))


def create_qeury(
    age,
    weight,
    height,
    gender,
    activity_level,
    goal,
    period,
):
    quaries = [
        str(age),
        str(weight),
        str(height),
        str(gender),
        str(activity_level),
        str(goal),
        str(period),
    ]
    return '&'.join(quaries)


def get_from_query():
    pass

#
# @app.route('/fill_cat', methods=['GET', 'POST'])
# def fill_cat():
#     items = {}
#     with open('name_cal_protein_fat_corb_gramm.pck', 'rb') as f:
#         items = pickle.load(f)
#     j = 0
#     print([items.keys()])
#
#     for cat_name in items.keys():
#         j += 1
#         print(cat_name)
#         cats = Category.query.filter_by(name=cat_name).all()
#         if len(cats) == 0:
#             cat = Category(
#                 name=cat_name
#             )
#         else:
#             cat = cats[0]
#         i = 0
#         for item in items[cat_name]:
#             i += 1
#             name, cal, protein, fat, corb, gramm, ref = item
#             print(name, cal, protein, fat, corb, gramm, ref)
#             print(f'{j}/{len(items.keys())}, {i}/{len(items[cat_name])}')
#             its = Item.query.filter_by(name=name).all()
#             if len(its) == 0:
#                 it = Item(
#                     name=name,
#                     calories=cal,
#                     protein=protein,
#                     fat=fat,
#                     carbohydrate=corb,
#                     gramm=gramm,
#                     link=ref
#                 )
#             else:
#                 it = its[0]
#             it.categories.append(cat)
#             db.session.add(it)
#     db.session.commit()
#

@app.route('/', methods=['GET', 'POST'])
def create_suggest():

    activity_levels_choices = [
        (el.id, el.name) for el in ActivityLevel.query.all()
    ]
    goals_choices = [
        (el.id, el.name) for el in Goal.query.all()
    ]
    periods_choices = [
        (el.id, el.name) for el in Period.query.all()
    ]

    form = forms.CreateSuggest()
    form.activity_level.choices = activity_levels_choices
    form.goal.choices = goals_choices
    form.period.choices = periods_choices
    if form.validate_on_submit():

        quary = create_qeury(
            age=form.age.data,
            weight=form.weight.data,
            height=form.height.data,
            gender=form.gender.data,
            activity_level=form.activity_level.data,
            goal=form.goal.data,
            period=form.period.data,
        )

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
#
#
# @app.route('/admin/eq_conf/<gender>', methods=['GET', 'POST'])
# def admin_eq_conf(gender):
#     if current_user.is_authenticated:
#
#         eq_conf = mtool.get_eq_conf(gender)
#
#         form = forms.EditEqConf()
#         if form.validate_on_submit():
#             const = form.const.data
#             c_weight = form.c_weight.data
#             c_height = form.c_height.data
#             c_age = form.c_age.data
#
#             new_eq_conf = {
#                 'const': const,
#                 'c_weight': c_weight,
#                 'c_height': c_height,
#                 'c_age': c_age,
#             }
#
#             mtool.set_eq_conf(new_eq_conf, gender)
#             return redirect(url_for('admin_eq_conf'))
#
#         return render_template(
#             'admin/eq_conf.html',
#             eq_conf=eq_conf,
#             title='Админ-панель',
#             form=form,
#         )
#
#     return redirect(url_for('create_suggest'))
#


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('create_suggest'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
