import framework
import conditions
import analysis
import random
import numpy as np
import time

# simulates a single game played given a set of conditions
def run_trial(condition):
    current_team_num = 0
    team_points = np.zeros(condition.team_num)
    for board_num in range(condition.board_num):
        board = condition.build_board(board_num + 1)
        while True in board.view_availability():
            # determine the category/question selected based on team's strategy
            current_team = condition.teams[current_team_num]
            rotated_points = np.roll(team_points, current_team_num)
            category = current_team.strategy(board, current_team.difficulty_scale, rotated_points)
            question = board.view_question_nums(category)

            # assign points based on distribution
            points = board.select(category)
            for team in np.roll(condition.teams, current_team_num):
                if random.random() <= team.correct_odds(question):
                    team_points[team] += points
                    break

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
        score_table[i, :] += new_vals

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
