from suggest_tool.paths import *
from suggest_tool.models import Recipe, Day, d1_recipe_types
import pickle 
import time
import pandas as pd
import copy


def build_day_menu():
    save_pck(1, UPDATE_PATH)

    t1 = time.time()

    recipes = load_pck(RECIPES_PATH)

    code_recipes = {}
    for r in recipes:
        code_recipes[r.code] = r
    save_pck(code_recipes, CODE_RECIPES_PATH)

    columns=['Завтрак', 'Обед', 'Перекус', 'Ужин', 'Калории', 'Белки', 'Жиры', 'Углеводы']

    day_menu = pd.DataFrame([], columns=columns)

    day_menu = day_menu.astype({
            'Завтрак': 'int32',
            'Обед': 'int32',
            'Перекус': 'int32',
            'Ужин': 'int32',
            'Калории': 'float16',
            'Белки': 'float16',
            'Жиры': 'float16',
            'Углеводы': 'float16',
    })

    breakfasts = []
    lunchs = []
    snackes = []
    dinners = []

    for r in recipes:
        if r.recipe_type.name == 'Завтрак':
            breakfasts.append(r)
        elif r.recipe_type.name == 'Обед':
            lunchs.append(r)
        elif r.recipe_type.name== 'Перекус':
            snackes.append(r)
        elif r.recipe_type.name == 'Ужин':
            dinners.append(r)

    print(len(breakfasts), len(lunchs), len(snackes), len(dinners))
    i = 0
    for b in breakfasts:
        for l in lunchs:
            for s in snackes:
                for d in dinners:
                    i += 1
                    if not len({b.code, l.code, s.code, d.code}) == 4:
                        continue
                    row = [
                        b.code,
                        l.code,
                        s.code,
                        d.code,
                        b.calories + l.calories + s.calories + d.calories,
                        b.protein + l.protein + s.protein + d.protein,
                        b.fat + l.fat + s.fat + d.fat,
                        b.corb + l.corb + s.corb + d.corb,
                    ]


                    print(f'{int(i * 100 / (len(breakfasts) * len(lunchs) * len(snackes) * len(dinners)))}%, {int(day_menu.memory_usage().sum() / 1000000)} MB')
                    day_menu = day_menu.append(pd.DataFrame([row], columns=columns))

    day_menu.to_pickle(DAY_MENU_PATH)

    print(f'time: {int(time.time() - t1)} sec')
    save_pck(2, UPDATE_PATH)

def get_menu(user):
    code_recipes = load_pck(CODE_RECIPES_PATH)
    eq_conf = load_pck(EQ_CONF_PATH)

    activity_levels = {al.abr: al for al in load_pck(ACTIVITY_LEVELS_PATH)}
    goals = {g.abr: g for g in load_pck(GOALS_PATH)}
    periods = {p.abr: p for p in load_pck(PERIODS_PATH)}

    user.fat_percent = (1 - user.fat_percent / 100)
    amount_of_calories = eq_conf['const']
    for k, v in eq_conf.items():
        if k == 'const':
            continue
        amount_of_calories += v * getattr(user, k[2:])

    amount_of_calories *= goals[user.goal].percent * activity_levels[user.activity_level].activity

    need_protein = amount_of_calories * goals[user.goal].pfc[0] / 4
    need_fat = amount_of_calories * goals[user.goal].pfc[1] / 9
    need_corb = amount_of_calories * goals[user.goal].pfc[2] / 4

    less = 1.2
    more = 0.8

    day_menu = pd.read_pickle(DAY_MENU_PATH)

    options = day_menu[
        (amount_of_calories * less >= day_menu['Калории']) & 
        (amount_of_calories * more <= day_menu['Калории']) &        
        (need_protein * less >= day_menu['Белки']) & 
        (need_protein * more <= day_menu['Белки']) &
        (need_fat * less >= day_menu['Жиры']) & 
        (need_fat * more <= day_menu['Жиры']) &
        (need_corb * less >= day_menu['Углеводы']) & 
        (need_corb * more <= day_menu['Углеводы'])
    ]
    print('s', options.shape[0])

    days = []
    i = 0
    rac = ['Завтрак', 'Обед', 'Перекус', 'Ужин']
    while len(days) < periods[user.period].days:
        opt = options.sample(frac=1)
        for n in rac:
            opt.drop_duplicates(subset=n, keep='first', inplace=True)

        lil_days = []
        for _, row in opt.iterrows():
            recipes = []
            for name in rac:
                r = copy.copy(code_recipes[row[name]])
                r.recipe_type = d1_recipe_types[name]
                recipes.append(r)

            i += 1
            day = Day(num=i, recipes=recipes)
            lil_days.append(day)

        days = days + lil_days


    return days[:periods[user.period].days]

def add_score(id_, score):
    pass