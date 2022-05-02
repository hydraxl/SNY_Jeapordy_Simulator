# SNY_Jeopardy_Simulator

Background:
  A group I'm in creates a version of Jeopardy where each of the three teams can only select the lowest point value question available in a given category. Additionally, steals are based on team order rather than speed. If team 1 gets a question wrong, team 2 will have the chance to steal first, and if team 2 gets it wrong then team 3 can attempt the question. If all three teams answer wrong, nobody gets the points. This projects analyzes the fairness of this version of the game. Specifically, does any one team have an inherent advantage due to going first, second, or third? If so, how significant is this advantage?

Methodology:
  I used a Monte Carlo simulation for each of several conditions to estimate the likelihood of winning for each team. The conditions included the approximate difficulty of each point value and category, modeled by the likelihood of a team answering correctly, as well as the strategy each team employed in picking the questions. Strategies included greedy algorithms, expected value, purely random, random weighted by point value, and random weighted by expected value. I also picked 3 models of question difficulty to run my tests on that I labeled as Easy, Medium, and Hard.

Results:
  ADD LATER
