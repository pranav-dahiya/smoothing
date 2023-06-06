import numpy as np

for alpha in [0, 1, 2, 3, 4]:
    for beta in [0, 1, 2, 4, 8]:
        with open('attack.txt', 'w') as f:
            f.write(f'{alpha}\n{beta}\n')
        rng = np.random.default_rng()
        with open(f'sts-2.1.2/data/alpha_{alpha}_beta_{beta}.txt', 'wb') as f:
            for _ in range(3125000):
                f.write(f'{rng.bit_generator.random_raw():064b}\n'.encode('ascii'))
