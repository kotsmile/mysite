import pickle

import suggest_tool.paths as paths


def load_pck(path):
    with open(path, 'rb') as file:
        return pickle.load(file)


def save_pck(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)


def get_recipe(code):
    code_recipes = load_pck(paths.CODE_RECIPES_PATH)
    return code_recipes[code]


def get_recipes(key=''):
    if key == '':
        breakfasts = load_pck(paths.BREAKFASTS_PATH)
        lunchs = load_pck(paths.LUNCHS_PATH)
        dinners = load_pck(paths.DINNERS_PATH)
        snackes = load_pck(paths.SNACKES_PATH)

        return breakfasts + lunchs + dinners + snackes

    elif key in paths.abr_to_path_rt.keys():
        return load_pck(paths.abr_to_path_rt[key])

    elif key == 'set':
        breakfasts = load_pck(paths.BREAKFASTS_PATH)
        lunchs = load_pck(paths.LUNCHS_PATH)
        dinners = load_pck(paths.DINNERS_PATH)
        snackes = load_pck(paths.SNACKES_PATH)

        return breakfasts, lunchs, dinners, snackes

    elif key == 'dict':
        return {k: get_recipes(key=k) for k in paths.abr_to_path_rt.keys()}

    elif key == 'dict_bld':
        return {
            k: get_recipes(key=k)
            for k in paths.abr_to_path_rt.keys()
            if not k == 'snack'
        }

    return [-1]


def set_recipes(abr, recipes):
    save_pck(recipes, paths.abr_to_path_rt[abr])


def add_recipe(new_recipe):
    recipes = get_recipes(key=new_recipe.recipe_type.abr)

    is_found = False
    for r in recipes:
        if (r.name == new_recipe.name
                and r.recipe_type.abr == new_recipe.recipe_type.abr):
            is_found = True
            break

    if not is_found:
        if len(recipes) == 0:
            new_recipe.code = 0
        else:
            new_recipe.code = max([r.code for r in recipes]) + 1
        recipes.append(new_recipe)
        set_recipes(new_recipe.recipe_type.abr, recipes)

    success = not is_found
    return success


def remove_recipe(code):
    recipes = get_recipes()

    for r in recipes:
        if r.code == code:
            abr = r.recipe_type.abr

    recipes = get_recipes(key=abr)
    new_recipes = []
    for r in recipes:
        if not r.code == code:
            new_recipes.append(r)

    set_recipes(abr, new_recipes)


def create_code_to_recipe():
    code_recipes = {}
    for r in get_recipes():
        code_recipes[r.code] = r
    save_pck(code_recipes, paths.CODE_RECIPES_PATH)


def get_activity_levels():
    return load_pck(paths.ACTIVITY_LEVELS_PATH)


def set_activity_levels(activity_levels):
    save_pck(activity_levels, paths.ACTIVITY_LEVELS_PATH)


def add_activity_level(new_activity_level):
    activity_levels = get_activity_levels()

    is_found = False
    for al in activity_levels:
        if al.abr == new_activity_level.abr:
            is_found = True
            break

    if not is_found:
        activity_levels.append(new_activity_level)
        set_activity_levels(activity_levels)

    success = not is_found
    return success


def remove_activity_level(abr):
    activity_levels = get_activity_levels()
    new_activity_levels = []

    for al in activity_levels:
        if not al.abr == abr:
            new_activity_levels.append(al)

    set_activity_levels(new_activity_levels)


def get_goals():
    return load_pck(paths.GOALS_PATH)


def set_goals(goals):
    save_pck(goals, paths.GOALS_PATH)


def add_goal(new_goal):
    goals = get_goals

    is_found = False
    for g in goals:
        if g.abr == new_goal.abr:
            is_found = True
            break

    if not is_found:
        goals.append(new_goal)
        set_goals(goals)

    success = not is_found
    return success


def remove_goal(abr):
    goals = get_goals()
    new_goals = []

    for g in goals:
        if not g.abr == abr:
            new_goals.append(g)

    set_goals(new_goals)


def get_periods():
    return load_pck(paths.PERIODS_PATH)


def set_periods(periods):
    save_pck(periods, paths.PERIODS_PATH)


def add_period(new_period):
    periods = get_periods()

    is_found = False
    for p in periods:
        if p.abr == new_period.abr:
            is_found = True
            break

    if not is_found:
        periods.append(new_period)
        set_periods(periods)

    success = not is_found
    return success


def remove_period(abr):
    periods = get_periods()
    new_periods = []

    for p in periods:
        if not p.abr == abr:
            new_periods.append(p)

    set_periods(new_periods)


def get_eq_conf(gender):
    if gender == 'm':
        return load_pck(paths.EQ_CONF_M_PATH)
    elif gender == 'f':
        return load_pck(paths.EQ_CONF_F_PATH)


def set_eq_conf(eq_conf, gender):
    if gender == 'm':
        save_pck(eq_conf, paths.EQ_CONF_M_PATH)
    elif gender == 'f':
        save_pck(eq_conf, paths.EQ_CONF_F_PATH)


def get_users():
    return load_pck(paths.USERS_PATH)


def set_users(users):
    save_pck(users, paths.USERS_PATH)


def add_user(new_user):
    users = get_users()
    users.append(new_user)
    set_users(users)
