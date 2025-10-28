import matplotlib.pyplot as plt

from qlearn import learn

RUNS = 30
x = [0]
x8 = [77, 71, 74, 80, 166, 81, 72, 83, 63, 83, 420, 67, 137, 50, 70, 103, 81, 80, 81, 249, 58, 670, 64, 75, 87, 68, 86, 79, 109, 87]
x4 = [10, 14, 77, 12, 48, 14, 8, 71, 13, 35, 20, 26, 6, 26, 22, 4, 58, 19, 20, 36, 21, 18, 16, 21, 8, 4, 16, 16, 27, 4]

exploration = ("state_counting", 1)
convergence_criteria = ("policy_delta", 3)

if len(x) == 0:
    for _ in range(RUNS):
        episode_count = learn(8, 1, 1, 0.9, exploration, convergence_criteria)
        x.append(episode_count)

print(x)

fig, axes = plt.subplots(nrows = 2, ncols = 1, sharex = True, figsize = (6, 8))
axes[0].boxplot(x4, vert = False)
axes[1].boxplot(x8, vert = False)

plt.tight_layout()
plt.show()
