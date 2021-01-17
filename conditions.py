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
        options = [i for i in range(len(availability)) if availability[i]]
        weights = [vals[i] for i in options]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
        weights = [vals[x][y] for x, y in options]
    return random.choices(options, weights=weights)[0]

# highest point value
def greedy(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    if type(board) == framework.Board:
        options = [i for i in range(len(availability)) if availability[i]]
        weights = [vals[i] for i in options]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
        weights = [vals[x][y] for x, y in options]
    return options[weights.index(max(weights))]

# stochastic expected value
def sev(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    if type(board) == framework.Board:
        nums = board.view_question_nums()
        options = [i for i in range(len(availability)) if availability[i]]
        weights = [vals[i] * difficulty_scale[nums[i]] for i in options]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
        weights = [vals[x][y] * difficulty_scale[y] for x, y in options]
    return random.choices(options, weights=weights)[0]

# expected value
def ev(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    if type(board) == framework.Board:
        nums = board.view_question_nums()
        options = [i for i in range(len(availability)) if availability[i]]
        weights = [vals[i] * difficulty_scale[nums[i]] for i in options]
    elif type(board) == framework.OpenBoard:
        options = [(x, y) for x in range(len(availability)) for y in range(len(availability[0])) if availability[x][y]]
        weights = [vals[x][y] * difficulty_scale[y] for x, y in options]
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


# Multiplier Functions
#   Input: Board Number
#   Output: Board Multiplier
# How much more than the first board are the questions worth
base_multiplier = lambda x: x
ones_multiplier = lambda x: 1


# Point Functions
#   Input: Question Number
#   Output: Question Value (unmultiplied)
base_points = lambda x: 100 * x
one_hundred_points = lambda x: 100


# Point Assigners
#   Determines scoring when team is asked question

# Determine which team to assign points
def std_give_pts(teams, question, points, rand_func):
    rand = rand_func()
    team_num = len(teams)
    new_points = np.zeros(team_num)
    odds = 0
    for i in range(team_num):
        odds += teams[i].difficulty_scale[question] * (1 - odds)
        if rand <= odds:
            new_points[i] += points
            break;
    return new_points

# New way of assigning points that lets all other teams attempt if first team fails
def split_give_pts(teams, question, points, rand_func):
    team_num = len(teams)
    new_points = np.zeros(team_num)
    scorers = []
    if rand_func() <= teams[0].difficulty_scale[question]: scorers.append(0)
    else: scorers += [i for i in range(1, len(teams)) if rand_func() <= teams[i].difficulty_scale[question]]
    for i in scorers: new_points[i] += points / len(scorers)
    return new_points


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
deterministic = framework.Condition(all_greedy, all_baseline, base_multiplier, base_points)


# List of all strategy functions
strategies = [('ev', all_ev), ('greedy', all_greedy), ('sev', all_sev), ('spv', all_spv)]

# List of all difficulty assigners
difficulties = [('easy', all_easy), ('medium', all_medium), ('hard', all_hard)]

# Dictionary of all conditions
compile_conditions = lambda multiplier_function=base_multiplier, point_function=base_points, board=framework.Board, point_assigner=std_give_pts, team_num=3, board_num=2, category_num=5, question_num=5: {diff_name + ' ' + strat_name: framework.Condition(strat, diff, multiplier_function, point_function, board, point_assigner, team_num, board_num, category_num, question_num) for strat_name, strat in strategies for diff_name, diff in difficulties}

std_conditions = compile_conditions()
split_assigner_conditions = compile_conditions(point_assigner=split_give_pts)
open_board_conditions = compile_conditions(board=framework.OpenBoard)
