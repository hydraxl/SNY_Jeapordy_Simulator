expect = lambda f, input, result: f(input) == result

class Board:
    def __init__(self, multiplier=1, category_num=5, question_num=5):
        self.questions = [0] * category_num
        self.available = [True] * category_num
        self.max = question_num
        self.multiplier = multiplier

    def select(self, category):
        self.questions[category] += 1
        if self.questions[category] == self.max: self.available[category] = False
        return self.questions[category] * 100 * self.multiplier

    view_values = lambda self: [100 * self.multiplier * (n + 1) for n in self.questions]
    view_availability = lambda self: self.available[:]
    view_question_nums = lambda self: self.questions[:]

class Team:
    def __init__(self, strategy, difficulty_scale, num):
        self.difficulty_scale = difficulty_scale
        self.strategy = strategy
        self.num = num

class Condition:
    def __init__(self, strategy_assigner, difficulty_scale_assigner, team_num=3, board_num=2, category_num=5, question_num=5):
        self.team_num = team_num
        self.question_num = question_num
        self.category_num = category_num
        self.teams = [Team(strategy_assigner(i, team_num), difficulty_scale_assigner(i, team_num)(question_num), i) for i in range(team_num)]
        self.board_num = board_num
