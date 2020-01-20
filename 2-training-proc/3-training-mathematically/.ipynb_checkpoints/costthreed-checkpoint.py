def f(area, w_1, w_2):
    return w_1*area + w_2

import numpy as np
def sigma(value):
    return 1/(1 + np.exp(-value))

def sum_of_squared_errors(paired_data, w_1, w_2):
    return sum([(target - sigma(f(feature, w_1, w_2)))**2 for (feature, target) in paired_data])

import pandas as pd
df = pd.read_csv('./cell_data.csv')
areas = df['mean_area'].tolist()
targets = df['is_cancerous'].tolist()

scaled_areas = [area/1000 for area in areas]

paired_data = list(zip(scaled_areas, targets))


# https://stackoverflow.com/questions/43800390/how-to-create-all-combinations-column-wise-for-multiple-variables-in-pandas/43800485
import itertools
import pandas as pd
val_range = [val/10 for val in list(range(-20, 20))]
A = val_range
B = val_range

a = [A, B]
idx = ['c{}'.format(i) for i in range(1, len(val_range)+1)]
data = list(itertools.product(*a))
df = pd.DataFrame(data, columns=list('ab')).T

x_vals = df.iloc[0, :]
y_vals = df.iloc[1, :]
# y_vals = df.b

z_vals =[sum_of_squared_errors(paired_data, w_1, w_2) for (w_1, w_2) in list(zip(x_vals, y_vals))]

import plotly.graph_objects as go
fig = go.Figure(data=[
    go.Mesh3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        colorbar_title='cost curve',
        colorscale=[[0, 'gold'],
                    [0.5, 'mediumturquoise'],
                    [1, 'magenta']],
        intensity=[0, 0.33, 0.66, 1],
        name='y',
        showscale=True
    )
])

fig.update_layout(scene = dict(
                    xaxis_title='w1',
                    yaxis_title='b',
                    zaxis_title='SSE'))