import framework
import random
import numpy as np
from itertools import permutations

# Strategies
#   Input: board
#   Output: question index

# pick randomly
def base_strat(board, difficulty_scale, current_scores):
    availability = board.view_availability()
    options = [i for i in range(len(availability)) if availability[i]]
    return random.choice(options)

# random weighted by point value
def by_points(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    weights = [vals[i] for i in range(len(vals)) if i in options]
    return random.choices(options, weights=weights)[0]

# highest point value
def highest(board, difficulty_scale, current_scores):
    vals = board.view_values()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    return max(options)

# random weighted by point value and odds of guessing correctly
def greedy_random(board, difficulty_scale, current_scores):
    vals = board.view_question_nums()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    weights = [vals[i] * difficulty_scale[vals[i]][0] for i in range(len(vals)) if availability[i]]
    return random.choices(options)[0]

def greedy_deterministic(board, difficulty_scale, current_scores):
    vals = board.view_question_nums()
    availability = board.view_availability()
    options = [i for i in range(len(vals)) if availability[i]]
    weights = [vals[i] * difficulty_scale[vals[i]][0] for i in range(len(vals)) if availability[i]]
    return options[weights.index(max(weights))]


# Difficulty Functions (odds of answering the question correctly by team)
#   Input: question_num
#   Output: array of likelihood of answering a question correctly by difficulty

# even distribution from easiest to hardest
scale_maker = lambda hardest, easiest: lambda question_num: np.array([hardest + ((easiest - hardest) / (question_num - 1)) * question for question in range(question_num)]) if question_num > 1 else (hardest + easiest) / 2

easy = scale_maker(1, 1)
medium = scale_maker(.5, 1)
hard = scale_maker(.3, .7)


# Strategy Assigners
#   Input: total number of teams, current team
#   Output: the strategy for the current team

# All teams use the same strategy
all_strat_x = lambda strat: lambda current, total: strat

all_base_strat = all_strat_x(base_strat)
all_by_points = all_strat_x(by_points)
all_highest = all_strat_x(highest)
all_greedy = all_strat_x(greedy_deterministic)
all_greedy_weighted = all_strat_x(greedy_random)


# Difficulty Assigners
#   Input: total number of teams, current team
#   Output: difficulty scale for current team

# All teams use the same strategy
all_scale_x = lambda scale: lambda current, total: scale

all_easy = all_scale_x(easy)
all_medium = all_scale_x(medium)
all_hard = all_scale_x(hard)


# Conditions
#   All of the conditions being analyzed
# Since easy difficult has all questions being answered correctly by the team
#   that chooses them, some strategies are made equivalent for easy difficulty
#   that are different on higher difficulties

# Always takes the highest point value and answers correctly
deterministic = framework.Condition(all_highest, all_easy)

# Chooses questions by greed with medium difficulty
medium_greedy = framework.Condition(all_greedy, all_medium)

# Chooses questions by greed with hard difficulty
hard_greedy = framework.Condition(all_greedy, all_hard)

# Chooses highest point value questions with medium difficulty
medium_highest = framework.Condition(all_highest, all_medium)

# Chooses highest point value questions with hard difficulty
hard_highest = framework.Condition(all_highest, all_hard)

# Question choice is random and weighted by point value, easy difficulty
easy_by_points = framework.Condition(all_by_points, all_easy)

# Question choice is random and weighted by point value, medium difficulty
medium_by_points = framework.Condition(all_by_points, all_medium)

# Question choice is random and weighted by point value, hard difficulty
hard_by_points = framework.Condition(all_by_points, all_hard)

# Question choice is random, easy difficulty
easy_random = framework.Condition(all_base_strat, all_easy)

# Question choice is random, medium difficulty
medium_random = framework.Condition(all_base_strat, all_medium)

# Question choice is random, hard difficulty
hard_random = framework.Condition(all_base_strat, all_hard)

# Question choice is random weighted by greed, medium difficulty
medium_random_greedy = framework.Condition(all_greedy_weighted, all_medium)

# Question choice is random weighted by greed, hard difficulty
hard_random = framework.Condition(all_greedy_weighted, all_hard)
