from numpy.random import PCG64Mod,
import matplotlib.pyplot as plt


rng = default_rng()
signs = [(rng.bit_generator.random_raw() >> 8) & 1 for _ in range(10000)]
print()
print(signs.count(0))
print(signs.count(1))

randoms = rng.normal(size=[10000])
plt.hist(randoms, bins=100)
plt.show()
