from suggest_tool.paths import *
from suggest_tool.models import *
import pickle 
import time
import pandas as pd
import copy
import random


def get_menu(user):

    code_recipes = load_pck(CODE_RECIPES_PATH)

    breakfasts = load_pck(BREAKFASTS_PATH)
    lunchs = load_pck(LUNCHS_PATH)
    dinners = load_pck(DINNERS_PATH)
    snackes = load_pck(SNACKES_PATH)

    eq_conf = load_pck(EQ_CONF_PATH)
    activity_levels = {al.abr: al for al in load_pck(ACTIVITY_LEVELS_PATH)}
    goals = {g.abr: g for g in load_pck(GOALS_PATH)}
    periods = {p.abr: p for p in load_pck(PERIODS_PATH)}


    min_metab = eq_conf['const']
    if user.gender == 'm':
        min_metab += 166 # from excel table for female

    for k, v in eq_conf.items():
        if k == 'const':
            continue
        min_metab += v * getattr(user, k[2:])

    total_of_cal = min_metab * goals[user.goal].percent if min_metab * goals[user.goal].percent >= 1200 else 1200

    error_percent_cal = 0.05
    error_percent_protein = 0.07
    error_percent_fat = 0.05
    error_percent_corb = 0.07

    search_error_percent_cal = 0.15
    search_error_percent_protein = 0.15
    search_error_percent_fat = 0.15
    search_error_percent_corb = 0.15

    cal_with_activity = total_of_cal * activity_levels[user.activity_level].activity

    # protein
    if user.gender == 'm':
        min_protein = user.weight * 1.5
        print(cal_with_activity)
        print(goals[user.goal].pfc[0] - 0.07)
        print(cal_with_activity * (goals[user.goal].pfc[0] - error_percent_protein) / 4)
    else:
        min_protein = 60

    if cal_with_activity * (goals[user.goal].pfc[0] - error_percent_protein) / 4 >= min_protein:
        min_need_protein = cal_with_activity * (goals[user.goal].pfc[0] - error_percent_protein) / 4
    else:
        min_need_protein = min_protein

    if cal_with_activity * (goals[user.goal].pfc[0] + error_percent_fat) / 4 < 2 * user.weight:
        max_need_protein = cal_with_activity * (goals[user.goal].pfc[0] + error_percent_fat) / 4
    else:
        max_need_protein = 2 * user.weight

    # fat
    if user.gender == 'm':
        min_fat = 40
    else:
        min_fat = 35

    if cal_with_activity * (goals[user.goal].pfc[1] - error_percent_fat) / 9 >= min_fat:
        min_need_fat = cal_with_activity * (goals[user.goal].pfc[1] - error_percent_fat) / 9
    else:
        min_need_fat = min_fat
    max_need_fat = cal_with_activity * (goals[user.goal].pfc[1] + error_percent_fat) / 9

    # corb
    min_need_corb = cal_with_activity * (goals[user.goal].pfc[2] - error_percent_corb) / 4
    max_need_corb = cal_with_activity * (goals[user.goal].pfc[2] + error_percent_corb) / 4

    rts = ['Завтрак', 'Обед', 'Ужин']

    recipes = {'Завтрак': breakfasts, 'Обед': lunchs, 'Ужин': dinners}

    for_types = goals[user.goal].for_types

    for_types_cpfc = {
        rt: (
            (cal_with_activity * (1 - error_percent_cal) * for_types[rt], cal_with_activity * (1 + error_percent_cal) * for_types[rt]),
            (min_need_protein * for_types[rt], max_need_protein * for_types[rt]),
            (min_need_fat * for_types[rt], max_need_fat * for_types[rt]),
            (min_need_corb * for_types[rt], max_need_corb * for_types[rt])
        ) for rt in rts
    }

    searched_recipes = {rt: [] for rt in rts}

    for rt in rts:
        for r in recipes[rt]:
            cal_cond = (
                for_types_cpfc[rt][0][0] * (1 - search_error_percent_cal) <=
                r.calories <= for_types_cpfc[rt][0][1]
            )
            protein_cond = (
                for_types_cpfc[rt][1][0] * (1 - search_error_percent_protein) <=
                r.protein <= for_types_cpfc[rt][1][1]
            )
            fat_cond = (
                for_types_cpfc[rt][2][0] * (1 - search_error_percent_fat) <=
                r.fat <= for_types_cpfc[rt][2][1]
            )
            corb_cond = (
                for_types_cpfc[rt][3][0] * (1 - search_error_percent_corb) <=
                r.corb <= for_types_cpfc[rt][3][1]
            )

            if cal_cond and protein_cond and fat_cond and corb_cond:
                searched_recipes[rt].append(r)

    good_pairs = {rt: [] for rt in rts}

    for rt in rts:
        for recipe in searched_recipes[rt]:
            random.shuffle(snackes)
            i = 0
            for snack in snackes:
                cal_cond = (
                    for_types_cpfc[rt][0][0] <= recipe.calories + snack.calories <= for_types_cpfc[rt][0][1]
                )
                protein_cond = (
                    for_types_cpfc[rt][1][0] <= recipe.protein + snack.protein <= for_types_cpfc[rt][1][1]
                )
                fat_cond = (
                    for_types_cpfc[rt][2][0] <= recipe.fat + snack.fat <= for_types_cpfc[rt][2][1]
                )
                corb_cond = (
                    for_types_cpfc[rt][3][0] <= recipe.corb + snack.corb <= for_types_cpfc[rt][3][1]
                )
                if cal_cond and protein_cond and fat_cond and corb_cond:
                    good_pairs[rt].append((recipe, snack))
                    i += 1
                    if i == 10:
                        break

    raw_good_pairs = {}
    for rt in rts:
        raw_good_pairs[rt] = good_pairs[rt].copy()
        random.shuffle(raw_good_pairs[rt])

    amount_of_days = periods[user.period].days
    days = []

    used_snackes = []
    for i in range(1, amount_of_days + 1):
        recipes_for_day = [] 
        for rt in rts:
            find = False
            while not find:

                if len(raw_good_pairs[rt]) == 0:
                    for rt in rts:
                        raw_good_pairs[rt] = good_pairs[rt].copy()
                    random.shuffle(raw_good_pairs[rt])
                    used_snackes = []

                if raw_good_pairs[rt][0][1] not in used_snackes:

                    recipes_for_day.append(raw_good_pairs[rt][0][0])
                    recipes_for_day.append(raw_good_pairs[rt][0][1])
                    used_snackes.append(raw_good_pairs[rt][0][1])
                    find = True

                raw_good_pairs[rt].pop(0)

        day = Day(num=i, recipes=recipes_for_day)
        days.append(day)


    
    return (
        days,
        f"{int(for_types_cpfc['Завтрак'][0][0] / for_types['Завтрак'])} - {int(for_types_cpfc['Завтрак'][0][1] / for_types['Завтрак'])}",
        f"{int(for_types_cpfc['Завтрак'][1][0] / for_types['Завтрак'])} - {int(for_types_cpfc['Завтрак'][1][1] / for_types['Завтрак'])}",
        f"{int(for_types_cpfc['Завтрак'][2][0] / for_types['Завтрак'])} - {int(for_types_cpfc['Завтрак'][2][1] / for_types['Завтрак'])}",
        f"{int(for_types_cpfc['Завтрак'][3][0] / for_types['Завтрак'])} - {int(for_types_cpfc['Завтрак'][3][1] / for_types['Завтрак'])}",
    )

    
def add_score(id_, score):
    pass