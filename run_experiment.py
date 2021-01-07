import framework
import conditions
import analysis
import random
import numpy as np
import time

# Determine which team to assign points
def assign_points(team_points, teams, question, rand_num):
    team_num = len(teams)
    odds = 0
    for i in range(team_num):
        odds += teams[i].difficulty_scale[question] * (1 - odds)
        if rand_num <= odds: return i
    return None

# simulates a single game played given a set of conditions
def run_trial(condition):
    current_team_num = 0
    team_points = np.zeros(condition.team_num)
    for i in range(condition.board_num):
        board = framework.Board(i + 1, condition.category_num, condition.question_num)
        while True in board.view_availability():
            # determine the category/question selected based on team's strategy
            rotated_points = np.roll(team_points, -current_team_num)
            rotated_teams = np.roll(condition.teams, -current_team_num)
            category = rotated_teams[0].strategy(board, rotated_teams[0].difficulty_scale, rotated_points)
            question = board.view_question_nums()[category]
            points = board.select(category)

            # assign points based on distribution
            winner = assign_points(rotated_points, rotated_teams, question, random.random())
            if winner != None: team_points[(winner + current_team_num) % condition.team_num] += points

            # cycle current_team_num
            current_team_num += 1
            current_team_num %= condition.team_num

    return team_points

# simulates n games played given a set of conditions
# saves results to .dat file - filename given in the condition
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
condition = conditions.hard_highest
data = run_condition(condition)
bin_func = analysis.by_gap(300)
analysis.print_data(data)
print('Win Odds: ' + str(analysis.win_odds(data)))
analysis.boxplot(data, "hard_highest")
analysis.histogram(data, bin_func, "hard_highest")
analysis.show()
