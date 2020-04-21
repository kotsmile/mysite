import pickle

USERS_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/users.pck'

DAY_MENU_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/day_menu.pck'

ACTIVITY_LEVELS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/activity_level.pck'
GOALS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/goals.pck'
PERIODS_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/periods.pck'
EQ_CONF_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/eq_conf.pck'
RECIPES_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/recipes.pck'
CODE_RECIPES_PATH =  '/home/kotsmile/mysite/venv/suggest_tool/tables/code_recipes.pck'

UPDATE_PATH = '/home/kotsmile/mysite/venv/suggest_tool/tables/update.pck'



def get_update():
    with open(UPDATE_PATH, 'rb') as file:
            return pickle.load(file)

def set_update(n):
    with open(UPDATE_PATH, 'wb') as file:
        pickle.dump(n, file)



def load_pck(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

def save_pck(obj, path):
    with open(path, 'wb') as file:
        pickle.dump(obj, file)
