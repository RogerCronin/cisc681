import matplotlib.pyplot as plt
import numpy as np

from qlearn import learn

RUNS = 30
x = []

SIZE = 4
SUCCESS_RATE = 0.75

exploration = ("epsilon_greedy", 0.1)
convergence_criteria = ("policy_delta", 3)

if len(x) == 0:
    for _ in range(RUNS):
        episode_count = learn(SIZE, SUCCESS_RATE, 0.05, 0.9, exploration, convergence_criteria, (10, -1, -0.05))
        x.append(episode_count)

print(x)
print(np.mean(x))
print(np.std(x))

"""
fig, ax = plt.subplots()
ax.boxplot([x_0_9, x_0_8, x_0_7, x_0_6])
ax.set_xticklabels(["0.9", "0.8", "0.7", "0.6"])

ax.set_xlabel("Success rate")
ax.set_ylabel("Episode count")

plt.tight_layout()
plt.show()
"""