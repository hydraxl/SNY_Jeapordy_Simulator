import conditions
import numpy as np
import matplotlib.pyplot as plt

load_scores = lambda name: np.loadtxt(open(name + '.dat'))

# Data analysis

# Trial Measurements
'UNTESTED'
winner = lambda trial_data: trial_data.index(max(trial_data)) if not max(trial_data) in trial_data[:].remove(max(trial_data)) else None

win_tie = lambda trial_data: [i for i, x in enumerate(trial_data) if x == max(trial_data)]

# Aggregate Measurements
def win_or_tie_odds(data):
    num_trials = np.shape(data)[0]
    win_counter = np.zeros(num_teams, dtype=int)
    for trial in data:
        for i in win_tie(trial): win_counter[i] += 1
    return win_counter / sum(win_counter)

def win_odds(data):
    win_counter = np.zeros(num_teams, dtype=int)
    for trial in data:
        if winner(trial) != None: win_counter[winner(trial)] += 1
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

def overlapping_histograms(data, name, bin_func):
    data = data.T
    num_teams = np.shape(data)[0]
    plt.figure()
    for i in range(num_teams): plt.hist(data[i], bins=bin_func(data), alpha=0.5, label="team " + str(i+1))
    plt.xlabel("Points Scored")
    plt.ylabel("Count")
    plt.title(name)
    plt.legend(loc='upper right')

def histogram_plot(data, bin_func):
    # Collate data into bins and sizes
    data = data.T
    bins = bin_func(data)
    hist_data = [np.histogram(team_data, bins=bins)[0] for team_data in data]
    bin_centers = [(bins[i] + bins[i + 1]) / 2 for i in range(len(bins) - 1)]
    print(bin_centers[0])

    # Plot data
    plt.figure()
    for i in range(len(hist_data)): plt.scatter(bin_centers, hist_data[i], label="team " + str(i + 1))
    plt.xlabel("Points Scored")
    plt.ylabel("Count")
    plt.title(name)
    plt.legend(loc='upper right')

def histogram_lines(data, name, bin_func):
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

def boxplot(data, name):
    plt.figure()
    plt.boxplot(data)
    plt.xlabel("Team Number")
    plt.ylabel("Points Scored")
    plt.title(name)
'''
# Bin Functions
# Data array must be transposed before entering
by_num = lambda num: lambda data: np.concatenate((np.arange(np.amin(data), np.amax(data), (np.amax(data) - np.amin(data)) / (num - 1)), np.array([np.amax(data)])))
by_gap = lambda gap: lambda data: np.arange(np.amin(data), np.amax(data) + gap, gap)

# Show data
condition = conditions.highest_fair50_condition
data = load_scores(condition.name)
bin_func = by_gap(100)
print_data(data)
print('Win Odds: ' + str(win_odds(data)))
#overlapping_histograms(data, condition.name, bin_func)
boxplot(data, condition.name)
#histogram_plot(data, condition.name, bin_func)
histogram_lines(data, condition.name, bin_func)
plt.show()
'''
test1 = [1, 2, 3]
#print(winner(test1))
print(win_tie(test1))
print()
test2 = [1, 2, 2]
#print(winner(test2))
print(win_tie(test2))
