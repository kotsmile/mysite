import pickle

USERS_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/users.pck'

DAY_MENU_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/menus/'

ACTIVITY_LEVELS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/activity_level.pck'
GOALS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/goals.pck'
PERIODS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/periods.pck'
EQ_CONF_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/eq_conf.pck'

BREAKFASTS_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/recipes/breakfast.pck'
LUNCHS_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/recipes/lunchs.pck'
DINNERS_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/recipes/dinners.pck'
SNACKES_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/recipes/snackes.pck'

CAT_REF_EDA_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/cat_ref_eda.pck'

CODE_RECIPES_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/code_recipes.pck'

def load_pck(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

def save_pck(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)

def add_recipe(path, recipe):
    r = load_pck(path)
    r.append(recipe)
    save_pck(r, path)