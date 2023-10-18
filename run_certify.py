import os

for alpha in [0, 1, 2, 3, 4]:
    for beta in [1, 2, 4, 8]:
        with open('attack.txt', 'w') as f:
            f.write(f'{alpha}\n{beta}\n')
        os.system(f'python code/certify.py cifar10 models/cifar10/cifar_resnet110/noise_0.50/checkpoint.pth.tar '
                  f'logs/alpha_{alpha}_beta_{beta}.log --noise gaussian --sigma 0.5 --skip 20 --batch 100')
