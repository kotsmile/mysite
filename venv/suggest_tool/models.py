from suggest_tool.paths import *
from suggest_tool.parser import get_all_from
import pickle

class ActivityLevel:
    def __init__(self, name, abr, activity):
        self.name = name
        self.abr = abr 
        self.activity = activity

class Goal:
    def __init__(self, name, abr, percent, pfc):
        self.name = name
        self.abr = abr 
        self.percent = percent
        self.pfc = pfc

class Period:
    def __init__(self, name, abr, days):
        self.name = name
        self.abr = abr 
        self.days = days

class User:
    def __init__(
        self, 
        id_=0, 
        age=0, 
        weight=0,
        height=0,
        fat_percent=0,
        activity_level=0,
        goal=0,
        period=0
    ):
        self.id_ = id_

        self.age = age
        self.weight = weight
        self.height = height

        self.fat_percent = fat_percent
        
        self.activity_level = activity_level
        self.goal = goal

        self.period = period

    def get_activity_level(self):
        return activity_level_sym[self.activity_level]

    def get_goal(self):
        return goal_sym[self.goal]

class Ingredient:
    def __init__(self, code):
        pass

class RecipeType:
    def __init__(self, name, abr):
        self.name = name
        self.abr = abr

class Day:
    def __init__(self, num, recipes):
        self.num = num
        self.recipes = recipes


BREAKFAST = RecipeType(name='Завтрак', abr='breakfast')
LUNCH = RecipeType(name='Обед', abr='lunch')
SNACK = RecipeType(name='Перекус', abr='snack')
DINNER = RecipeType(name='Ужин', abr='dinner')

recipe_types = [
    BREAKFAST,
    LUNCH,
    SNACK,
    DINNER
]

d_recipe_types = {
    'breakfast': BREAKFAST,
    'lunch': LUNCH,
    'snack': SNACK,
    'dinner': DINNER
}

d1_recipe_types = {
    'Завтрак': BREAKFAST,
    'Обед': LUNCH,
    'Перекус': SNACK,
    'Ужин': DINNER
}

class Recipe:
    def __init__(self, link, recipe_type):
        self.recipe_type = recipe_type
        self.link = link
        self.code, self.name, self.time, self.calories, self.protein, self.fat, self.corb = get_all_from(link)
