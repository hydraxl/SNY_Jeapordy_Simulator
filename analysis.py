import numpy as np
import matplotlib.pyplot as plt

'''
load_scores = lambda name: np.loadtxt(open(name + '.dat'))
'''

# Trial Measurements
winner = lambda trial_data: np.where(trial_data == max(trial_data))[0][0] if len(np.where(trial_data == max(trial_data))[0]) == 1 else None

win_tie = lambda trial_data: np.where(trial_data == max(trial_data))[0]

# difference between first and second place
advantage = lambda trial_data: max(trial_data) - sorted(trial_data)[-2]

# difference between each team and first place
amt_behind = lambda trial_data: [max(trial_data) - trial_data[team] for team in trial_data]


# Aggregate Measurements

# takes a statistic of every trial
collate = lambda f, data: [f(trial) for trial in data]

# counts the instances of n in a list recursively
count_n = lambda n, data: sum([count_n(n, i) if type(i) == list or type(i) == np.ndarray else 1 if i == n else 0 for i in data])

def win_or_tie_odds(data):
    num_teams = np.shape(data)[1]
    win_counter = np.zeros(num_teams)
    winners = collate(win_tie, data)
    for i in range(num_teams): win_counter[i] += count_n(i, winners)
    return win_counter / sum(win_counter)

def win_odds(data):
    win_counter = np.zeros(np.shape(data)[1], dtype=int)
    for trial in data: win_counter[winner(trial)] += 1
    return win_counter / sum(win_counter)

means = lambda data: np.mean(data, axis=0)
medians = lambda data: np.median(data, axis=0)
stddevs = lambda data: np.std(data, axis=0)
iqr = lambda data: np.subtract(*np.percentile(data, [75, 25], axis=0))

# Data representations
def print_data(data):
    print("Means: " + str(means(data)))
    print("Medians: " + str(medians(data)))
    print("Stddevs: " + str(stddevs(data)))
    print("IQRs: " + str(iqr(data)))

def histogram(data, bin_func, name='', purpose='Points Scored'):
    data = data.T
    num_teams = np.shape(data)[0]
    bins = bin_func(data)
    hist_data = [np.histogram(team_data, bins=bins)[0] for team_data in data]

    # Plot data
    plt.figure()
    left, right = bins[:-1], bins[1:]
    X = np.array([left, right]).T.flatten()
    for i in range(num_teams):
        Y = np.array([hist_data[i], hist_data[i]]).T.flatten()
        plt.plot(X, Y, label="team " + str(i + 1))
    plt.xlabel(purpose)
    plt.ylabel("Count")
    plt.title(name)
    plt.legend(loc='upper right')

def boxplot(data, name='', purpose='Points Scored'):
    plt.figure()
    plt.boxplot(data)
    plt.xlabel('Team Number')
    plt.ylabel(purpose)
    plt.title(name)

def show(): plt.show()

# Bin Functions
# Data array must be transposed before entering
by_num = lambda num: lambda data: np.concatenate((np.arange(np.amin(data), np.amax(data), (np.amax(data) - np.amin(data)) / (num - 1)), np.array([np.amax(data)])))
by_gap = lambda gap: lambda data: np.arange(np.amin(data), np.amax(data) + gap, gap)
