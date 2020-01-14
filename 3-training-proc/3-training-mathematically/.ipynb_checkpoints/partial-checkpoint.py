import pandas as pd
import itertools
val_range = [val/10 for val in list(range(-20, 20))]
A = val_range
B = val_range

a = [A, B]
idx = ['c{}'.format(i) for i in range(1, len(val_range)+1)]
data = list(itertools.product(*a))
df = pd.DataFrame(data, columns=list('ab')).T

x_vals = df.iloc[0, :]
y_vals = df.iloc[1, :]