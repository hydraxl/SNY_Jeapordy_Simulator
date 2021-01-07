import numpy as np
import matplotlib.pyplot as plt

'''
load_scores = lambda name: np.loadtxt(open(name + '.dat'))
'''

# Trial Measurements
def winner(trial_data):
    highest = max(trial_data)
    index = np.where(trial_data == highest)[0]
    return index[0] if len(index) == 1 else None

win_tie = lambda trial_data: np.where(trial_data == highest)[0]

# Aggregate Measurements
def win_or_tie_odds(data):
    win_counter = np.zeros(np.shape(data)[1], dtype=int)
    for trial in data:
        for i in win_tie(trial): win_counter[i] += 1
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

def histogram(data, bin_func, name=''):
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
    plt.xlabel("Points Scored")
    plt.ylabel("Count")
    plt.title(name)
    plt.legend(loc='upper right')

def boxplot(data, name=''):
    plt.figure()
    plt.boxplot(data)
    plt.xlabel("Team Number")
    plt.ylabel("Points Scored")
    plt.title(name)

def show(): plt.show()

# Bin Functions
# Data array must be transposed before entering
by_num = lambda num: lambda data: np.concatenate((np.arange(np.amin(data), np.amax(data), (np.amax(data) - np.amin(data)) / (num - 1)), np.array([np.amax(data)])))
by_gap = lambda gap: lambda data: np.arange(np.amin(data), np.amax(data) + gap, gap)
