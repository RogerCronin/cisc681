import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Polygon

# Random 4x4x4 grid: [row][col][direction] with values from 0 to 1
data = np.random.rand(4, 4, 4)

# Colormap
cmap = plt.colormaps["viridis"]  # or any other colormap
norm = colors.Normalize(0, 1)  # Normalize values to 0–1 range

fig, ax = plt.subplots(figsize=(6, 6))

# Loop through the grid
for i in range(4):  # rows
    for j in range(4):  # columns
        # Cell origin (bottom-left corner of the square)
        x0, y0 = j, 3 - i  # Flip y to match display from top-left
        
        # Square center
        cx, cy = x0 + 0.5, y0 + 0.5

        # Triangle definitions
        triangles = {
            0: [(x0, y0+1), (x0+1, y0+1), (cx, cy)],     # Up
            1: [(x0, y0), (x0+1, y0), (cx, cy)],         # Down
            2: [(x0, y0), (x0, y0+1), (cx, cy)],         # Left
            3: [(x0+1, y0), (x0+1, y0+1), (cx, cy)],     # Right
        }

        # Draw triangles with color
        for direction in range(4):
            value = data[i, j, direction]
            color = cmap(norm(value))
            triangle = Polygon(triangles[direction], color=color, edgecolor='black', linewidth=0.5)
            ax.add_patch(triangle)

# Set limits and hide axes
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
ax.set_aspect('equal')
ax.axis('off')

# Optional: Add a colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04, label='Value')

plt.tight_layout()
plt.show()