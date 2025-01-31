# evaluate a smoothed classifier on a dataset
import argparse
import os
import pickle
from collections import defaultdict
import setGPU
import numpy as np
from datasets import get_dataset, DATASETS, get_num_classes
from core import Smooth
from noise import *
from time import time
import torch
import datetime
from architectures import get_architecture

parser = argparse.ArgumentParser(description='Certify many examples')
parser.add_argument("dataset", choices=DATASETS, help="which dataset")
parser.add_argument("base_classifier", type=str, help="path to saved pytorch model of base classifier")
parser.add_argument("outfile", type=str, help="output file")
parser.add_argument("--noise", choices=NOISE_FUNCTIONS.keys(), help="noise function")
parser.add_argument("--noise_arg", type=float, help="arguments for noise function")
parser.add_argument("--sigma", type=float, help="sigma for original noise function")
parser.add_argument("--batch", type=int, default=5000, help="batch size")
parser.add_argument("--skip", type=int, default=1, help="how many examples to skip")
parser.add_argument("--max", type=int, default=-1, help="stop after this many examples")
parser.add_argument("--split", choices=["train", "test"], default="test", help="train or test set")
parser.add_argument("--N0", type=int, default=100)
parser.add_argument("--N", type=int, default=10000, help="number of samples to use")
parser.add_argument("--alpha", type=float, default=0.001, help="failure probability")
args = parser.parse_args()

if __name__ == "__main__":
    # load the base classifier
    checkpoint = torch.load(args.base_classifier)
    base_classifier = get_architecture(checkpoint["arch"], args.dataset)
    base_classifier.load_state_dict(checkpoint['state_dict'])

    # create the smooothed classifier g
    if args.noise:
        print(args.noise_arg or args.sigma)
        noise = NOISE_FUNCTIONS[args.noise](args.noise_arg or args.sigma)
        smoothed_classifier = Smooth(base_classifier, get_num_classes(args.dataset), noise=noise, sigma=args.sigma)
    else:
        smoothed_classifier = Smooth(base_classifier, get_num_classes(args.dataset), sigma=args.sigma)

    # prepare output file
    f = open(args.outfile, 'w+')
    print("idx\tlabel\tpredict\tradius\tpABar\tcorrect\ttime", file=f, flush=True)

    # iterate through the dataset
    dataset = get_dataset(args.dataset, args.split)

    radius_list = list()
    results = defaultdict(list)
    for i in range(len(dataset)):

        # only certify every args.skip examples, and stop after args.max examples
        if i % args.skip != 0:
            continue
        if i == args.max:
            break

        (x, label) = dataset[i]

        before_time = time()
        # certify the prediction of g around x
        x = x.cuda()
        prediction, radius, pABar = smoothed_classifier.certify(x, args.N0, args.N, args.alpha, args.batch)
        after_time = time()
        correct = int(prediction == label)

        if prediction != Smooth.ABSTAIN:
            radius_list.append(radius[-1]['radius'])
        time_elapsed = str(datetime.timedelta(seconds=(after_time - before_time)))
        print("{}\t{}\t{}\t{:.3}\t{:.3}\t{}\t{}".format(
            i, label, prediction, radius[-1]['radius'], pABar, correct, time_elapsed), file=f, flush=True)

        results['i'].append(i)
        results['label'].append(label)
        results['prediction'].append(prediction)
        results['radius'].append(radius)
        results['pABar'].append(pABar)
        results['correct'].append(correct)

    f.close()

    with open(f'{args.outfile}.pickle', 'wb') as f:
        pickle.dump(results, f)

    print(args.outfile, np.mean(radius_list), np.std(radius_list))
