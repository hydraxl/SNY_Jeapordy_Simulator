import framework
import conditions
import analysis
import random
import numpy as np
import time

# simulates a single game played given a set of conditions
def run_trial(condition):
    current_team = 0
    team_points = np.zeros(condition.team_num)
    for board_num in range(condition.board_num):
        board = condition.build_board(board_num + 1)
        while True in board.view_availability():
            # determine the category/question selected based on team's strategy
            current_strat = condition.teams[current_team].strategy
            rotated_points = np.roll(team_points, current_team)
            rotated_dist = np.roll(condition.point_dist, current_team, axis=1)
            category = current_strat(board, rotated_dist, rotated_points)

            # assign points based on distribution
            team_odds = condition.point_dist[board.view_question_nums()[category]]
            points = board.select(category)
            for i in range(condition.team_num):
                answerer = (current_team + i) % condition.team_num
                if random.random() <= team_odds[answerer]:
                    team_points[answerer] += points
                    break

            # cycle current_team
            current_team += 1
            current_team %= condition.team_num

    return team_points

# simulates n games played given a set of conditions
# saves results to .dat file - filename given in the condition
def run_condition(condition, n=1000):
    current_time = time.time()
    seconds = 1
    score_table = np.zeros((n, condition.team_num))
    start = 0
    '''
    try:
        # If data already exists for this condition, add to it
        old = np.loadtxt(open(condition.name + '.dat'))
        start = len(old)
        score_table = np.concatenate((old, score_table), axis=0)
    '''

    for i in range(n):
        # Run trials
        new_vals = run_trial(condition)
        score_table[start + i, :] += new_vals

        # Mark time so code is verifiably still running
        if (time.time() - current_time) >= seconds:
            print("." * (seconds % 3 + 1))
            seconds += 1

    # Save data to text file
    #np.savetxt(condition.name + '.dat', score_table)
    return score_table
