import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

for alpha in [1, 2, 3, 4]:
    with open('attack.txt', 'w') as f:
        f.write(f'{alpha}\n-1\n-1\n')
    rng = np.random.default_rng()
    samples = rng.normal(0, 0.25, size=[100000])
    _, bins, _ = plt.hist(samples, bins=100, density=True)
    bin_centers = 0.5*(bins[1:] + bins[:-1])
    plt.plot(bin_centers, stats.norm.pdf(bin_centers, 0, 0.25), linewidth=6)
    plt.xticks([])
    plt.yticks([])
    # plt.savefig(f'alpha_{alpha}.pdf')
    plt.show()

for beta in [0, 1, 2, 4]:
    with open('attack.txt', 'w') as f:
        f.write(f'-1\n{beta}\n-1\n')
    rng = np.random.default_rng()
    samples = rng.normal(0, 0.25, size=[100000])
    _, bins, _ = plt.hist(samples, bins=100, density=True)
    bin_centers = 0.5*(bins[1:] + bins[:-1])
    plt.plot(bin_centers, stats.norm.pdf(bin_centers, 0, 0.25), linewidth=6)
    plt.xticks([])
    plt.yticks([])
    # plt.savefig(f'beta_{beta}.pdf')
    plt.show()

for gamma in [0, 1, 2, 4]:
    with open('attack.txt', 'w') as f:
        f.write(f'-1\n-1\n{gamma}\n')
    rng = np.random.default_rng()
    samples = rng.normal(0, 0.25, size=[100000])
    _, bins, _ = plt.hist(samples, bins=100, density=True)
    bin_centers = 0.5*(bins[1:] + bins[:-1])
    plt.plot(bin_centers, stats.norm.pdf(bin_centers, 0, 0.25), linewidth=6)
    plt.xticks([])
    plt.yticks([])
    # plt.savefig(f'gamma_{gamma}.pdf')
    plt.show()
