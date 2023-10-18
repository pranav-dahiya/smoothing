#!/bin/bash

python code/train.py cifar10 cifar_resnet110 models --noise bernoulli --noise_args 0.5
python code/train.py cifar10 cifar_resnet110 models --noise abs_gaussian --noise_args 0.125
python code/train.py cifar10 cifar_resnet110 models --noise abs_gaussian --noise_args 0.25
python code/train.py cifar10 cifar_resnet110 models --noise abs_gaussian --noise_args 0.5
python code/train.py cifar10 cifar_resnet110 models --noise abs_gaussian --noise_args 1.0