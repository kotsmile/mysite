import random

import suggest_tool.formulas as formulas
import suggest_app.models as models
# import suggest_tool.models_tool as mtool


def calculate_ideal_weight(user):

    a = user.age
    gender = user.gender
    h = user.height
    w = user.weight
    wg = user.wg
    cg = user.cg

    formulas_list = [
        formulas.miller_fromula,
        formulas.robbinson_fromula,
        formulas.devin_fromula,
        formulas.potton_index,
        formulas.brock_index,
        formulas.brock_brugsha_index,
        formulas.brock_age,
        formulas.mochamed_fromula,
        formulas.brock_index_k,
        formulas.born_index,
        formulas.monerota_formula,
        formulas.kreffer_formula,
        formulas.strach_formula,
        formulas.lorenz_fromula,
        formulas.haliva_fromula,
        formulas.nagshra_fromula,
        formulas.cooper_fromula
    ]

    sum_w = 0
    n = 0
    for f in formulas_list:
        el = f(h, w, wg, cg, a, gender)
        if not el == -1:
            n += 1
            sum_w += el

    return sum_w / n


def calculate_calories(user):
    eq_conf = models.EqConf.query.filter_by(gender=user.gender).first()
    goal = models.Goal.query.filter_by(id=user.goal).first()

    activity_level = models.ActivityLevel.query.filter_by(id=user.activity_level).first()

    min_metab = user.height * eq_conf.height + user.weight * eq_conf.weight \
        + user.age * eq_conf.age + eq_conf.const

    cal_with_activity = min_metab * goal.percent / 100 if min_metab * \
        goal.percent / 100 >= 1200 else 1200

    cal_with_activity *= activity_level.activity_level

    return cal_with_activity


def fat_loose(fat_percent):
    if 0.29 <= fat_percent:
        return 1.15 / 7
    elif 0.22 <= fat_percent < 0.29:
        return 0.6 / 7
    elif 0.17 <= fat_percent < 0.22:
        return 0.35 / 7
    elif fat_percent < 0.16:
        return 0.15 / 7


IDEAL_FAT_PERCANT = 0.22
LOOSE_CALORIES_PER_DAY = 200 / 7


def get_plan(user):



    ideal_weight = calculate_ideal_weight(user)

    real_calories = user.real_calories
    goal_calories = calculate_calories(user)

    fat_now = user.weight - ideal_weight * (1 - IDEAL_FAT_PERCANT)
    fat_percent = fat_now / user.weight
    init_fat = fat_percent

    calories_now = real_calories
    weight_now = user.weight

    days = 0
    weight_values = []
    calorie_values = []
    fat_percents = []

    while calories_now >= goal_calories:
        days += 1
        weight_values.append(weight_now)
        calorie_values.append(calories_now)
        fat_percents.append(fat_percent)

        if LOOSE_CALORIES_PER_DAY > calories_now - goal_calories:

            calories_now -= calories_now - goal_calories
            weight_now -= fat_loose(fat_percent)
            fat_now -= fat_loose(fat_percent)

            fat_percent = fat_now / weight_now

            break
        else:

            calories_now -= LOOSE_CALORIES_PER_DAY
            weight_now -= fat_loose(fat_percent)
            fat_now -= fat_loose(fat_percent)

            fat_percent = fat_now / weight_now

    days += 1
    weight_values.append(weight_now)
    calorie_values.append(calories_now)
    fat_percents.append(fat_percent)

    calories_now = goal_calories
    weight_now -= fat_loose(fat_percent)

    fat_now = weight_now - ideal_weight * (1 - IDEAL_FAT_PERCANT)
    fat_percent = fat_now / weight_now

    while weight_now > ideal_weight:
        days += 1
        weight_values.append(weight_now)
        calorie_values.append(calories_now)
        fat_percents.append(fat_percent)

        weight_now -= fat_loose(fat_percent)
        fat_now -= fat_loose(fat_percent)

        fat_percent = fat_now / weight_now

    # weight_values.append(weight_now)
    # calorie_values.append(calories_now)
    # fat_percents.append(fat_percent)


    return weight_values, calorie_values, fat_percents, user.real_calories, goal_calories, user.weight, ideal_weight, init_fat, IDEAL_FAT_PERCANT, days

# choices=[
#     ('usual', 'Обычный'),
#     ('vegan', 'Веганство'),
#     ('vegat', 'Вегетарианство'),
#     ('siroed', 'Сыроедение'),
# ],
# User.query.filter_by(login=form.login.data).first()
# ActivityLevel.query.all()
# eq_conf = models.EqConf.query.filter_by(gender=user.gender).first()
# goal = models.Goal.query.filter_by(id=user.goal).first()


def get_pfc(calories, user, part=1):
    error_percent_cal = 0.05
    error_percent_protein = 0.07
    error_percent_fat = 0.05
    error_percent_carb = 0.07
    goal = models.Goal.query.filter_by(id=user.goal).first()
    # protein
    if user.gender == 'm':
        min_protein = user.weight * 1.5
    else:
        min_protein = 60

    if calories * (goal.protein_percent / 100 - error_percent_protein) / 4 >= min_protein:
        min_need_protein = calories * (goal.protein_percent / 100 - error_percent_protein) / 4
    else:
        min_need_protein = min_protein

    if calories * (goal.protein_percent / 100 + error_percent_protein) / 4 < 2 * user.weight:
        max_need_protein = calories * (goal.protein_percent / 100 + error_percent_protein) / 4
    else:
        max_need_protein = 2 * user.weight

    # fat
    if user.gender == 'm':
        min_fat = 40
    else:
        min_fat = 35

    if calories * (goal.fat_percent / 100 - error_percent_fat) / 9 >= min_fat:
        min_need_fat = calories * (goal.fat_percent / 100 - error_percent_fat) / 9
    else:
        min_need_fat = min_fat
    max_need_fat = calories * (goal.fat_percent / 100 + error_percent_fat) / 9

    # corb
    min_need_carb = calories * (goal.carbohydrate_percent / 100 - error_percent_carb) / 4
    max_need_carb = calories * (goal.carbohydrate_percent / 100 + error_percent_carb) / 4

    return [
        (
            calories * (1 - error_percent_cal) * part,
            calories * (1 + error_percent_cal) * part,
        ),
        (min_need_protein * part, max_need_protein * part),
        (min_need_fat * part, max_need_fat * part),
        (min_need_carb * part, max_need_carb * part)
    ]


def get_menu_on_day(calories, user):

    name_vegan = 'Веганские продукты (без яиц и молока)'
    name_vegat = 'Вегетарианские продукты'
    name_syroed = 'Продукты для сыроедения'
    error_percent_cal = 0.05
    abr_to_name = {
        'usual': -1,
        'vegan': name_vegan,
        'vegat': name_vegat,
        'siroed': name_syroed,
    }
    types = [
        models.MealType.query.filter_by(name='Завтрак').first(),
        models.MealType.query.filter_by(name='Обед').first(),
        models.MealType.query.filter_by(name='Ужин').first()
    ]

    for t in types:
        print(t.name)
        combinations = models.Combination.query.filter_by(meal_type=t).all()
        packs_item_groups = [c.item_groups for c in combinations]
        for item_groups in packs_item_groups:
            items_for_item_groups = []
            for ig in item_groups:
                if abr_to_name[user.eater_type] == -1:
                    valid_items = set()
                    for c in models.Category.query.all():
                        valid_items.update(set(c.items.all()))
                else:
                    valid_items = models.Category.query.filter_by(
                        name=abr_to_name[user.eater_type]).first().items
                filtered_items_by_group = []
                for item in valid_items:
                    if item.item_group == ig:
                        filtered_items_by_group.append(item)

                items_for_item_groups.append((ig, filtered_items_by_group))
            correct_items_for_item_groups = []

            for ig, items in items_for_item_groups:
                params_percent = get_pfc(
                    calories, user, part=t.percent_of_CPFC_on_day / 100 * ig.percent / 100
                )
                print(params_percent)
                correct_items = []
                for it in items:
                    print(it.calories, it.protein, it.fat, it.carbohydrate)
                    try:
                        min_gramms_on_calories = it.gramm * params_percent[0][0] / it.calories
                        max_gramms_on_calories = it.gramm * params_percent[0][1] / it.calories

                        min_gramms_on_protein = it.gramm * params_percent[1][0] / it.protein
                        max_gramms_on_protein = it.gramm * params_percent[1][1] / it.protein

                        min_gramms_on_fat = it.gramm * params_percent[2][0] / it.fat
                        max_gramms_on_fat = it.gramm * params_percent[2][1] / it.fat

                        min_gramms_on_carb = it.gramm * params_percent[3][0] / it.carbohydrate
                        max_gramms_on_carb = it.gramm * params_percent[3][1] / it.carbohydrate
                    except ZeroDivisionError:
                        continue

                    print(min_gramms_on_calories, min_gramms_on_protein, min_gramms_on_fat, min_gramms_on_carb)
                    print(max_gramms_on_calories, max_gramms_on_protein, max_gramms_on_fat, max_gramms_on_carb)
                    min_gramms = max([
                        min_gramms_on_calories,
                        min_gramms_on_protein,
                        min_gramms_on_fat,
                        min_gramms_on_carb
                    ])

                    max_gramms = min([
                        max_gramms_on_calories,
                        max_gramms_on_protein,
                        max_gramms_on_fat,
                        max_gramms_on_carb
                    ])
                    print('-----')
                    print(min_gramms, max_gramms)
                    print('-----')
                    if max_gramms > min_gramms:
                        correct_gramms = (max_gramms + min_gramms) / 2
                        correct_items.append((correct_gramms, it))
                    else:
                        continue
                correct_items_for_item_groups.append((ig, correct_items))
            print(correct_items_for_item_groups)


# class EqConf(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     gender = db.Column(db.String(64))
#     const = db.Column(db.Float)
#     weight = db.Column(db.Float)
#     height = db.Column(db.Float)
#     age = db.Column(db.Float)

#
# def get_menu(user):
#
#     eq_conf = mtool.get_eq_conf(gender=user.gender)
#
#     activity_levels = {al.abr: al for al in mtool.get_activity_levels()}
#     goals = {g.abr: g for g in mtool.get_goals()}
#     periods = {p.abr: p for p in mtool.get_periods()}
#
#     min_metab = eq_conf['const']
#
#     for k, v in eq_conf.items():
#         if k == 'const':
#             continue
#         min_metab += v * getattr(user, k[2:])
#
#     cal_with_activity = min_metab * goals[user.goal].percent if min_metab * \
#         goals[user.goal].percent >= 1200 else 1200
#
#     error_percent_cal = 0.05
#     error_percent_protein = 0.07
#     error_percent_fat = 0.05
#     error_percent_corb = 0.07
#
#     search_error_percent_cal = 0.15
#     search_error_percent_protein = 0.15
#     search_error_percent_fat = 0.15
#     search_error_percent_corb = 0.15
#
#     cal_with_activity *= activity_levels[user.activity_level].activity
#
#     # protein
#     if user.gender == 'm':
#         min_protein = user.weight * 1.5
#     else:
#         min_protein = 60
#
#     if cal_with_activity * (goals[user.goal].pfc[0] - error_percent_protein) / 4 >= min_protein:
#         min_need_protein = cal_with_activity * (goals[user.goal].pfc[0] - error_percent_protein) / 4
#     else:
#         min_need_protein = min_protein
#
#     if cal_with_activity * (goals[user.goal].pfc[0] + error_percent_fat) / 4 < 2 * user.weight:
#         max_need_protein = cal_with_activity * (goals[user.goal].pfc[0] + error_percent_fat) / 4
#     else:
#         max_need_protein = 2 * user.weight
#
#     # fat
#     if user.gender == 'm':
#         min_fat = 40
#     else:
#         min_fat = 35
#
#     if cal_with_activity * (goals[user.goal].pfc[1] - error_percent_fat) / 9 >= min_fat:
#         min_need_fat = cal_with_activity * (goals[user.goal].pfc[1] - error_percent_fat) / 9
#     else:
#         min_need_fat = min_fat
#     max_need_fat = cal_with_activity * (goals[user.goal].pfc[1] + error_percent_fat) / 9
#
#     # corb
#     min_need_corb = cal_with_activity * (goals[user.goal].pfc[2] - error_percent_corb) / 4
#     max_need_corb = cal_with_activity * (goals[user.goal].pfc[2] + error_percent_corb) / 4
#
#     recipes = mtool.get_recipes(key='dict_bld')
#
#     for_types = goals[user.goal].for_types
#
#     for_types_cpfc = {
#         rt: (
#             (
#                 cal_with_activity * (1 - error_percent_cal) * for_types[rt],
#                 cal_with_activity * (1 + error_percent_cal) * for_types[rt]
#             ),
#             (
#                 min_need_protein * for_types[rt],
#                 max_need_protein * for_types[rt]
#             ),
#             (
#                 min_need_fat * for_types[rt],
#                 max_need_fat * for_types[rt]
#             ),
#             (
#                 min_need_corb * for_types[rt],
#                 max_need_corb * for_types[rt]
#             )
#         ) for rt in recipes.keys()
#     }
#
#     searched_recipes = {rt: [] for rt in recipes.keys()}
#
#     for rt in recipes.keys():
#         for r in recipes[rt]:
#             cal_cond = (
#                 for_types_cpfc[rt][0][0] * (1 - search_error_percent_cal)
#                 <= r.calories <= for_types_cpfc[rt][0][1]
#             )
#             protein_cond = (
#                 for_types_cpfc[rt][1][0] * (1 - search_error_percent_protein)
#                 <= r.protein <= for_types_cpfc[rt][1][1]
#             )
#             fat_cond = (
#                 for_types_cpfc[rt][2][0] * (1 - search_error_percent_fat)
#                 <= r.fat <= for_types_cpfc[rt][2][1]
#             )
#             corb_cond = (
#                 for_types_cpfc[rt][3][0] * (1 - search_error_percent_corb)
#                 <= r.corb <= for_types_cpfc[rt][3][1]
#             )
#
#             if cal_cond and protein_cond and fat_cond and corb_cond:
#                 searched_recipes[rt].append(r)
#
#     good_pairs = {rt: [] for rt in recipes.keys()}
#
#     for rt in recipes.keys():
#         for recipe in searched_recipes[rt]:
#             random.shuffle(snackes)
#             i = 0
#             for snack in snackes:
#                 cal_cond = (
#                     for_types_cpfc[rt][0][0] <= recipe.calories
#                     + snack.calories <= for_types_cpfc[rt][0][1]
#                 )
#                 protein_cond = (
#                     for_types_cpfc[rt][1][0] <= recipe.protein
#                     + snack.protein <= for_types_cpfc[rt][1][1]
#                 )
#                 fat_cond = (
#                     for_types_cpfc[rt][2][0] <= recipe.fat + snack.fat
#                     <= for_types_cpfc[rt][2][1]
#                 )
#                 corb_cond = (
#                     for_types_cpfc[rt][3][0] <= recipe.corb + snack.corb
#                     <= for_types_cpfc[rt][3][1]
#                 )
#                 if cal_cond and protein_cond and fat_cond and corb_cond:
#                     good_pairs[rt].append((recipe, snack))
#                     i += 1
#                     if i == 10:
#                         break
#
#     raw_good_pairs = {}
#     for rt in recipes.keys():
#         raw_good_pairs[rt] = good_pairs[rt].copy()
#         random.shuffle(raw_good_pairs[rt])
#         if len(raw_good_pairs[rt]) == 0:
#             return -1
#
#     amount_of_days = periods[user.period].days
#     days = []
#
#     used_snackes = []
#     for i in range(1, amount_of_days + 1):
#         recipes_for_day = []
#         for rt in recipes.keys():
#             find = False
#             while not find:
#
#                 if len(raw_good_pairs[rt]) == 0:
#                     for rt in recipes.keys():
#                         raw_good_pairs[rt] = good_pairs[rt].copy()
#                     random.shuffle(raw_good_pairs[rt])
#                     used_snackes = []
#
#                 if raw_good_pairs[rt][0][1] not in used_snackes:
#
#                     recipes_for_day.append(raw_good_pairs[rt][0][0])
#                     recipes_for_day.append(raw_good_pairs[rt][0][1])
#                     used_snackes.append(raw_good_pairs[rt][0][1])
#                     find = True
#
#                 raw_good_pairs[rt].pop(0)
#
#         day = Day(num=i, recipes=recipes_for_day)
#         days.append(day)
#
#     return (
#         days,
#         f"{int(for_types_cpfc['breakfast'][0][0] / for_types['breakfast'])} - "
#         + f"{int(for_types_cpfc['breakfast'][0][1] / for_types['breakfast'])}",
#         f"{int(for_types_cpfc['breakfast'][1][0] / for_types['breakfast'])} - "
#         + f"{int(for_types_cpfc['breakfast'][1][1] / for_types['breakfast'])}",
#         f"{int(for_types_cpfc['breakfast'][2][0] / for_types['breakfast'])} - "
#         + f"{int(for_types_cpfc['breakfast'][2][1] / for_types['breakfast'])}",
#         f"{int(for_types_cpfc['breakfast'][3][0] / for_types['breakfast'])} - "
#         + f"{int(for_types_cpfc['breakfast'][3][1] / for_types['breakfast'])}",
#     )
