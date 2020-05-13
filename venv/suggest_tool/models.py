
class User:
    def __init__(
        self,
        query=0,
        age=0,
        gender=0,
        weight=0,
        height=0,
        wg=0,
        cg=0,
        real_calories=0,
        activity_level=0,
        eater_type=0,
        goal=0,
    ):
        if not query == 0:
            (age, gender, weight, height,
             wg, cg, real_calories, activity_level,
             eater_type, goal) = query.split('-')

        self.age = int(age)
        self.gender = gender
        self.weight = float(weight)
        self.height = float(height)
        self.wg = float(wg)
        self.cg = float(cg)
        self.real_calories = float(real_calories)
        self.activity_level = float(activity_level)
        self.eater_type = eater_type
        self.goal = goal

    def to_query(self):
        queries = [
            str(self.age),
            str(self.gender),
            str(self.weight),
            str(self.height),
            str(self.wg),
            str(self.cg),
            str(self.real_calories),
            str(self.activity_level),
            str(self.eater_type),
            str(self.goal),
        ]
        return '-'.join(queries)
