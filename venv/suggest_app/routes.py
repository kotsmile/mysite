# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, jsonify

from flask_login import current_user, login_user, logout_user

from suggest_app import app, db

import suggest_app.models as models
from suggest_app.models import ActivityLevel, Goal, Item, Category
import suggest_app.forms as forms
from suggest_app.forms import RegistrationForm

import suggest_tool.calculator as calculator
from suggest_tool.models import User

import pickle

import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin')

    form = forms.LoginForm()
    if form.validate_on_submit():
        admin = models.User.query.filter_by(login=form.login.data).first()
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


@app.route('/', methods=['GET', 'POST'])
def create_suggest():

    activity_levels_choices = [
        (str(el.id), el.name) for el in ActivityLevel.query.all()
    ]
    goals_choices = [
        (str(el.id), el.name) for el in Goal.query.all()
    ]
    form = forms.CreateSuggest()
    form.activity_level.choices = activity_levels_choices
    form.goal.choices = goals_choices
    if form.validate_on_submit():
        user = User(
            age=form.age.data,
            gender=form.gender.data,
            weight=form.weight.data,
            height=form.height.data,
            wg=form.wg.data,
            cg=form.cg.data,
            real_calories=form.real_calories.data,
            activity_level=form.activity_level.data,
            eater_type=form.eater_type.data,
            goal=form.goal.data,
        )

        return redirect(f'/suggest/' + user.to_query())

    return render_template(
        'enter_user_data.html',
        title='Данные пользователя',
        form=form
    )


def get_img_obj(x, y, x_label, y_label, hy):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.grid()
    axis.plot(x, y, '-ro')
    axis.axhline(y=hy)
    ticks_week = [1] + [i * 7 for i in range(1, (max(x)) // 7 + 1)]
    axis.set_xticks(ticks_week)
    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)

    png_image_B64_string = "data:image/png;base64,"
    png_image_B64_string += base64.b64encode(png_image.getvalue()).decode('utf8')

    return png_image_B64_string


@app.route('/suggest/<query>')
def suggest(query):
    print(query)

    user = User(query=query)

    weight_values, calorie_values, fat_percents, init_calories, goal_calories, init_weight, goal_weight, init_fat_percent, goal_fat_percent, days = calculator.get_plan(user)

    image_w = get_img_obj(
        x=range(1, len(weight_values) + 1),
        y=weight_values,
        x_label='День',
        y_label='Вес, кг',
        hy=goal_weight,
    )
    image_с = get_img_obj(
        x=range(1, len(calorie_values) + 1),
        y=calorie_values,
        x_label='День',
        y_label='Норма калорий на день, ккал',
        hy=goal_calories,
    )
    image_f = get_img_obj(
        x=range(1, len(fat_percents) + 1),
        y=[i * 100 for i in fat_percents],
        x_label='День',
        y_label='Процент жира, %',
        hy=goal_fat_percent * 100,
    )
    calculator.get_menu_on_day(calorie_values[0], user)
    return render_template(
        'suggest.html',
        image_w=image_w,
        image_c=image_с,
        image_f=image_f,
        init_calories=init_calories,
        goal_calories=goal_calories,
        init_weight=init_weight,
        goal_weight=goal_weight,
        init_fat_percent=init_fat_percent,
        goal_fat_percent=goal_fat_percent,
        days=days,


    )


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
