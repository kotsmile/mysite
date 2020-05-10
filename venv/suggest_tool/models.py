from suggest_tool.parser import parse_page


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
