import framework
import conditions
import analysis
import random
import numpy as np
import time

# Returns sequence 1 element at a time, then repeats
def test_seq(seq):
    internal_generator = (lambda seq: [(yield n) for n in seq])()
    return lambda: next(internal_generator)

# simulates a single game played given a set of conditions
def run_trial(condition):
    current_team_num = 0
    team_points = np.zeros(condition.team_num)
    for i in range(condition.board_num):
        board = condition.board(i + 1, condition.category_num, condition.question_num)
        while True in board.view_availability():
            # determine the category/question selected based on team's strategy
            rotated_points = np.roll(team_points, -current_team_num)
            rotated_teams = np.roll(condition.teams, -current_team_num)
            if type(board) == framework.Board:
                category = rotated_teams[0].strategy(board, rotated_teams[0].difficulty_scale, rotated_points)
                question = board.view_question_nums()[category]
                points = board.select(category)
            elif type(board) == framework.OpenBoard:
                category, question = rotated_teams[0].strategy(board, rotated_teams[0].difficulty_scale, rotated_points)
                points = board.select(category, question)

            # assign points based on distribution
            team_points += np.roll(condition.point_assigner(rotated_teams, question, points, random.random), current_team_num)

            # cycle current_team_num
            current_team_num += 1
            current_team_num %= condition.team_num

    return team_points

# simulates n games played given a set of conditions
def run_condition(condition, n=1000):
    '''
    current_time = time.time()
    seconds = 1
    '''
    score_table = np.zeros((n, condition.team_num))
    for i in range(n):
        # Run trials
        new_vals = run_trial(condition)
        score_table[i] += new_vals

        '''
        # Mark time so code is verifiably still running
        if (time.time() - current_time) >= seconds:
            print("." * (seconds % 3 + 1))
            seconds += 1
        '''
    '''
    # Save data to text file
    np.savetxt(condition.name + '.dat', score_table)
    '''
    return score_table


# Show data
def analyze_condition(condition, name=''):
    print(name)
    data = run_condition(condition)
    win_distances = analysis.collate(analysis.amt_behind, data)
    advantages = analysis.collate(analysis.advantage, data)
    #bin_func = analysis.by_gap(300)
    #analysis.print_data(data)
    print('Win Odds: ' + str(analysis.win_odds(data)))
    print('Mean Scores: ' + str(analysis.means(data)))
    print('Mean Distance from Win: ' + str(analysis.means(win_distances)))
    print('Mean Difference between First and Second: ' + str(analysis.means(advantages)))
    #analysis.boxplot(data, name)
    #analysis.histogram(data, bin_func, name)
    print('\n')
    return analysis.win_odds(data)

#for name, condition in conditions.split_assigner_conditions.items(): analyze_condition(condition, name)
for name, condition in conditions.std_conditions.items(): analyze_condition(condition, name)

#print(run_trial(conditions.deterministic))
#analyze_condition(conditions.easy_greedy, "easy")
#analyze_condition(conditions.medium_greedy, "medium")
#analyze_condition(conditions.hard_greedy, "hard")
#analysis.show()
