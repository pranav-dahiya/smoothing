import numpy as np
import os
from time import sleep
from numpy.random import PCG64, MT19937, Philox, SFC64
from multiprocessing import Pool


def run_and_save(filename, n):
    # run test
    tests = 1000
    if n == 10**8:
        tests = 100
    with os.popen(f'./assess {n}', 'w') as f:
        sleep(2)
        f.write('0\n')
        sleep(2)
        f.write(f"{os.path.join('data/', filename)}\n")
        sleep(2)
        f.write('0\n')
        sleep(2)
        f.write('111110000000000')
        sleep(2)
        f.write('0\n')
        sleep(2)
        f.write(f'{tests}\n')
        sleep(2)
        f.write('0\n')
    # move file
    os.system(f'cp experiments/AlgorithmTesting/finalAnalysisReport.txt ../data_{n}/{os.path.basename(filename)}')


def generate_data(filename, bitgen, alpha=-1, gamma=-1, beta=-1):
    # generate data
    with open('attack.txt', 'w') as f:
        f.write(f'{alpha}\n{beta}\n{gamma}\n')
    rng = np.random.Generator(bitgen())
    with open(os.path.join('data/', filename), 'wb') as f:
        for _ in range(int(10**10 / 64)+1):
            f.write(f'{rng.bit_generator.random_raw():064b}\n'.encode('ascii'))


def run_test(bitgen, alpha=-1, beta=-1, gamma=-1):
    if alpha >= 0:
        filename = f'alpha_{alpha}.txt'
    elif beta >= 0:
        filename = f'beta_{beta}.txt'
    elif gamma >= 0:
        filename = f'gamma_{gamma}.txt'
    else:
        filename = f'{bitgen.__name__}.txt'
    basedir = f'sts-2.1.2_{os.getpid()}'
    os.system(f'cp -R sts-2.1.2/ {basedir}/')
    os.chdir(basedir)
    generate_data(filename, bitgen, alpha=alpha, beta=beta, gamma=gamma)
    for pow in [7]:
        n = 10**pow
        if not(os.path.exists(f'../data_{n}/{filename}')):
            run_and_save(filename, n)
    os.chdir('..')
    # os.system(f'rm -Rf {basedir}')


params = [[-1, -1, -1]]
# params.extend([[alpha, -1, -1] for alpha in [0, 1, 2, 4]])
params.extend([[-1, beta, -1] for beta in [0, 1, 2, 4]])
# params.extend([[-1, -1, gamma] for gamma in [1, 2, 3, 4]])


with Pool(13) as p:
    for args in params:
        p.apply_async(run_test, (PCG64, *args))
    # for bitgen in [MT19937, Philox, SFC64]:
    #     p.apply_async(run_test, (bitgen, ))
    p.close()
    p.join()
