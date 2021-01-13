import framework
import random
import numpy as np
from itertools import permutations

# Strategies
#   Input: board
#   Output: question index

# pick randomly
def unweighted(board, difficulty_scale, current_scores):
    availability = board.view_availability()
    if type(board) == framework.Board:
        options = [i for i in range(len(availability)) if availability[i]]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
    return random.choice(options)

# stochastically weighted by point value
def spv(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    if type(board) == framework.Board:
        options = [i for i in range(len(vals)) if availability[i]]
        weights = [vals[i] for i in range(len(vals)) if availability[i]]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
        weights = [vals[x][y] for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
    return random.choices(options, weights=weights)[0]

# highest point value
def greedy(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    return max(options)

# stochastic expected value
def sev(board, difficulty_scale, current_scores):
    vals = board.view_question_nums()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    weights = [vals[i] * difficulty_scale[vals[i]] for i in range(len(vals)) if availability[i]]
    return random.choices(options)[0]

# expected value
def ev(board, difficulty_scale, current_scores):
    vals = board.view_question_nums()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    weights = [vals[i] * difficulty_scale[vals[i]] for i in range(len(vals)) if availability[i]]
    return options[weights.index(max(weights))]

'''
# greedy, avoid 3rd question
def not_3rd(board, difficulty_scale, current_scores):
    vals = board.view_question_nums()
    availability = board.view_availability()
'''

# Difficulty Functions (odds of answering the question correctly by team)
#   Input: question_num
#   Output: array of likelihood of answering a question correctly by difficulty

# even distribution from easiest to hardest
scale_maker = lambda hardest, easiest: lambda question_num: np.array([hardest + ((easiest - hardest) / (question_num - 1)) * question for question in range(question_num)]) if question_num > 1 else (hardest + easiest) / 2

baseline = scale_maker(1, 1)
easy = scale_maker(.7, .9)
medium = scale_maker(.5, .9)
hard = scale_maker(.3, .9)

# Strategy Assigners
#   Input: total number of teams, current team
#   Output: the strategy for the current team

# All teams use the same strategy
all_strat_x = lambda strat: lambda current, total: strat

all_unweighted = all_strat_x(unweighted)
all_spv = all_strat_x(spv)
all_greedy = all_strat_x(greedy)
all_ev = all_strat_x(ev)
all_sev = all_strat_x(sev)


# Difficulty Assigners
#   Input: total number of teams, current team
#   Output: difficulty scale for current team

# All teams use the same strategy
all_scale_x = lambda scale: lambda current, total: scale

all_baseline = all_scale_x(baseline)
all_easy = all_scale_x(easy)
all_medium = all_scale_x(medium)
all_hard = all_scale_x(hard)


# Conditions
#   All of the conditions being analyzed
# Since easy difficult has all questions being answered correctly by the team
#   that chooses them, some strategies are made equivalent for easy difficulty
#   that are different on higher difficulties

# Always takes the highest point value and answers correctly
deterministic = framework.Condition(all_greedy, all_baseline)

# Dictionary of all conditions
def compile_conditions(board=framework.Board, point_assigner=framework.std_give_pts, team_num=3, board_num=2, category_num=5, question_num=5):
    return {'easy ev': framework.Condition(all_ev, all_easy, board, point_assigner, team_num, board_num, category_num, question_num),
    'medium ev': framework.Condition(all_ev, all_medium, board, point_assigner, team_num, board_num, category_num, question_num),
    'hard ev': framework.Condition(all_ev, all_hard, board, point_assigner, team_num, board_num, category_num, question_num),
    'easy greedy': framework.Condition(all_greedy, all_easy, board, point_assigner, team_num, board_num, category_num, question_num),
    'medium greedy': framework.Condition(all_greedy, all_medium, board, point_assigner, team_num, board_num, category_num, question_num),
    'hard greedy': framework.Condition(all_greedy, all_hard, board, point_assigner, team_num, board_num, category_num, question_num),
    'easy sev': framework.Condition(all_sev, all_easy, board, point_assigner, team_num, board_num, category_num, question_num),
    'medium sev': framework.Condition(all_sev, all_medium, board, point_assigner, team_num, board_num, category_num, question_num),
    'hard sev': framework.Condition(all_sev, all_hard, board, point_assigner, team_num, board_num, category_num, question_num),
    'easy spv': framework.Condition(all_spv, all_easy, board, point_assigner, team_num, board_num, category_num, question_num),
    'medium spv': framework.Condition(all_spv, all_medium, board, point_assigner, team_num, board_num, category_num, question_num),
    'hard spv': framework.Condition(all_spv, all_hard, board, point_assigner, team_num, board_num, category_num, question_num)}

std_conditions = compile_conditions()
split_assigner_conditions = compile_conditions(point_assigner=framework.split_give_pts)
