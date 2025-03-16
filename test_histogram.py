import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# Create a random number generator with a fixed seed for reproducibility
rng = np.random.default_rng(19680801)


N_points = 100000
n_bins = 20

# Generate two normal distributions
dist1 = rng.standard_normal(N_points)
dist2 = 0.4 * rng.standard_normal(N_points) + 5
print(dist1)
print(dist2)

fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# We can set the number of bins wSith the *bins* keyword argument.
axs[0].hist(dist1, bins=n_bins)
axs[1].hist(dist2, bins=n_bins)

plt.show()

#%%
notes = [10, 12, 6, 17, 15, 14, 15, 16, 17, 13, 15, 10, 16, 16, 16, 16]
plt.hist(notes, range = (0, 20), bins=50) 
plt.xticks(range(0, 21, 2))



plt.show()