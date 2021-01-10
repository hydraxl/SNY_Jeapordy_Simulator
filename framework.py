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


# Determine which team to assign points
def std_give_pts(team_points, teams, question, rand_func):
    rand = rand_func()
    team_num = len(teams)
    odds = 0
    for i in range(team_num):
        odds += teams[i].difficulty_scale[question] * (1 - odds)
        if rand <= odds: return [i]
    return []

# New way of assigning points that lets all other teams attempt if first team fails
def split_give_pts(team_points, teams, question, rand_func):
    team_num = len(teams)
    if rand_func() <= teams[0].difficulty_scale[question]: return [0]
    return [i for i in range(1, len(teams)) if rand_func() <= teams[i].difficulty_scale[question]]


class Condition:
    def __init__(self, strategy_assigner, difficulty_scale_assigner, point_assigner=std_give_pts, team_num=3, board_num=2, category_num=5, question_num=5):
        self.team_num = team_num
        self.question_num = question_num
        self.category_num = category_num
        self.teams = [Team(strategy_assigner(i, team_num), difficulty_scale_assigner(i, team_num)(question_num), i) for i in range(team_num)]
        self.board_num = board_num
        self.point_assigner = point_assigner
