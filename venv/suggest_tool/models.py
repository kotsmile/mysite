from suggest_tool.parser import parse_page


class ActivityLevel:
    def __init__(self, name, abr, activity):
        self.name = name
        self.abr = abr
        self.activity = activity


class Goal:
    def __init__(self, name, abr, percent, pfc, breakfast, lunch, dinner):
        self.name = name
        self.abr = abr
        self.percent = percent
        self.pfc = pfc
        self.for_types = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner
        }


class Period:
    def __init__(self, name, abr, days):
        self.name = name
        self.abr = abr
        self.days = days


class User:
    def __init__(
        self,
        age=0,
        weight=0,
        height=0,
        activity_level=0,
        goal=0,
        period=0,
        gender=0,
    ):

        self.age = age
        self.weight = weight
        self.height = height

        self.activity_level = activity_level
        self.goal = goal

        self.period = period
        self.gender = gender


class Ingredient:
    def __init__(self, code):
        pass


class Day:
    def __init__(self, num, recipes):
        self.num = num
        self.recipes = recipes


class RecipeType:
    def __init__(self, name, abr):
        self.name = name
        self.abr = abr


# class Recipe:
#     def __init__(self, link, recipe_type, code=0):
#         self.recipe_type = recipe_type
#         self.link = link
#         self.code = code
#         self.name, self.time, self.calories, self.protein, self.fat, self.corb = parse_page(link)
#

class Recipe:
    def __init__(self, link, recipe_type, code=0):
        self.recipe_type = recipe_type
        self.link = link
        self.code = code
        self.name, self.time, self.calories, self.protein, self.fat, self.corb, self.img_link, self.amount, self.ings, self.plan = parse_page(
            link)


BREAKFAST = RecipeType(name='Завтрак', abr='breakfast')
LUNCH = RecipeType(name='Обед', abr='lunch')
DINNER = RecipeType(name='Ужин', abr='dinner')
SNACK = RecipeType(name='Перекус', abr='snack')

recipe_types = [
    BREAKFAST,
    LUNCH,
    DINNER,
    SNACK,
]


abr_rt = {
    'b': BREAKFAST,
    'l': LUNCH,
    'd': DINNER,
    's': SNACK,
}

abr_to_recipe_type = {
    'breakfast': BREAKFAST,
    'lunch': LUNCH,
    'dinner': DINNER,
    'snack': SNACK,
}

d1_recipe_types = {
    'Завтрак': BREAKFAST,
    'Обед': LUNCH,
    'Ужин': DINNER,
    'Перекус': SNACK,
}
