#!/bin/bash

python code/certify.py cifar10 models/cifar10/resnet110/noise_1.00/checkpoint.pth.tar logs/gaussian_1.0.log --noise gaussian --noise_args 1.0 --skip 20
python code/certify.py cifar10 models/cifar10/cifar_resnet110/laplace_1.0/checkpoint.pth.tar logs/laplace_1.0.log --noise laplace --noise_args 1.0 --skip 20
python code/certify.py cifar10 models/cifar10/cifar_resnet110/uniform_1.0/checkpoint.pth.tar logs/uniform_1.0.log --noise uniform --noise_args 1.0 --skip 20
python code/certify.py cifar10 models/cifar10/cifar_resnet110/bernoulli_0.5/checkpoint.pth.tar logs/bernoulli_0.5.log --noise bernoulli --noise_args 0.5 --skip 20
python code/certify.py cifar10 models/cifar10/cifar_resnet110/abs_gaussian_1.0/checkpoint.pth.tar logs/abs_gaussian_1.0.log --noise abs_gaussian --noise_args 1.0 --skip 20
