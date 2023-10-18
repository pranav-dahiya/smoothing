from collections import defaultdict
import os

sorted_files = ['baseline.txt', 'gamma_1.txt', 'gamma_2.txt', 'gamma_3.txt', 'gamma_4.txt',
                'beta_0.txt', 'beta_1.txt', 'beta_2.txt', 'beta_4.txt',
                'alpha_0.txt', 'alpha_1.txt', 'alpha_2.txt', 'alpha_4.txt']

dirname = 'old_data'
files = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
full_results = dict()
tests = list()
for filename in sorted(files):
    results = defaultdict(list)
    with open(os.path.join(dirname, filename)) as f:
        text = f.readlines()
        for line in text[7:]:
            data = [val for val in line.split() if '*' not in val]
            if not data:
                break
            try:
                results[data[-1]].append(int(data[-2].split('/')[0]))
            except ValueError:
                pass
    results = {key: min(val) for key, val in results.items() if val}
    full_results[filename] = results
    tests = results.keys()

for key in tests:
    print(key)
    print(' & '.join(str(full_results[file][key]) for file in sorted_files))