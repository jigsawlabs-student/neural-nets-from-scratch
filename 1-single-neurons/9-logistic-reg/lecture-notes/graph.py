import plotly
from plotly.offline import iplot, init_notebook_mode
from error import rss
init_notebook_mode(connected=True)

def trace(data, mode = 'markers', name="data"):
    x_values = list(map(lambda point: point['x'],data))
    y_values = list(map(lambda point: point['y'],data))
    return {'x': x_values, 'y': y_values, 'mode': mode, 'name': name}

def line_function_trace(line_function, x_values, mode = 'line', name = 'line function'):
    values = line_function_data(line_function, x_values)
    values.update({'mode': mode, 'name': name})
    return values

def line_function_data(line_function, x_values):
    y_values = list(map(lambda x: line_function(x), x_values))
    return {'x': x_values, 'y': y_values}

def model_and_actuals(m, b, x_values, y_values):
    y_hats = list(map(lambda x: m*x + b, x_values))
    actual_trace = trace_values(x_values, y_hats, mode= 'line')
    model_trace_built = model_trace(m, b, x_values, y_values)
    return [model_trace_built, actual_trace]

def model_trace(m, b, x_values, y_values):
    y_hats = list(map(lambda x: m*x + b, x_values))
    return trace_values(x_values, y_hats, mode="lines")

def errors_from_model(m, b, x_values, y_values):
    y_hats = list(map(lambda x: m*x + b, x_values))
    y_values_y_hats = list(zip(y_values, y_hats))
    errors = list(map(lambda pair: pair[0] - pair[1], y_values_y_hats))
    return error_line_traces(x_values, y_values, errors)

def trace_rss(m, b, x_values, y_values):
    rss_calc = rss(m, b, x_values, y_values)
    return dict(
        x=['RSS'],
        y=[rss_calc],
        type='bar'
    )

def plot_side_by_side(left_traces, right_traces):
    from plotly import tools
    fig = tools.make_subplots(rows=1, cols=2)
    [fig.append_trace(left_trace, 1, 1) for left_trace in left_traces]
    [fig.append_trace(right_trace, 1, 2) for right_trace in right_traces]
    plotly.offline.iplot(fig)


def pair_colors(left_traces, right_traces, colors = ['red', 'yellow', 'blue', 'orange', 'green']):
    pairs = list(zip(left_traces, right_traces))
    for i in range(0, len(pairs)):
        selection = i%5
        pairs[i][0]['marker'] = {'color': colors[selection]}
        pairs[i][1]['marker'] = {'color': colors[selection]}
    return (left_traces, right_traces)

def traces_from_model(m, b, x_values, y_values):
    y_hats = list(map(lambda x: m*x + b, x_values))
    actual_trace = trace_values(x_values, y_values)
    model_trace = trace_values(x_values, y_hats, mode="lines")
    return [actual_trace, model_trace]

def m_b_data(m, b, x_values):
    y_values = list(map(lambda x: m*x + b, x_values))
    return {'x': x_values, 'y': y_values}

def m_b_trace(m, b, x_values, mode = 'line', name = 'line function'):
    values = m_b_data(m, b, x_values)
    values.update({'mode': mode, 'name': name})
    return values
    
def plot(traces, layout = {}):
    if not isinstance(traces, list): raise TypeError('first argument must be a list.  Instead is', traces)
    plotly.offline.iplot({'data': traces, 'layout': layout})

def build_layout(x_range = None, y_range = None, options = {}):
    layout = {}
    if isinstance(x_range, list): layout.update({'xaxis': {'range': x_range}})
    if isinstance(y_range, list): layout.update({'yaxis': {'range': y_range}})
    layout.update(options)
    return layout


def trace_values(x_values, y_values, mode = 'markers', name="data", text = []):
    return {'x': x_values, 'y': y_values, 'mode': mode, 'name': name, 'text': text}


def make_subplots(one_one_traces = [], one_two_traces = [], two_one_traces = [], two_two_traces = []):
    if two_one_traces or two_two_traces:
        fig = tools.make_subplots(rows=2, cols=2)
    else:
        fig = tools.make_subplots(rows=1, cols=2)
    for trace in one_one_traces:
        fig.append_trace(trace, 1, 1)
    for trace in one_two_traces:
        fig.append_trace(trace, 1, 2)
    for trace in two_one_traces:
        fig.append_trace(trace, 1, 1)
    for trace in two_two_traces:
        fig.append_trace(trace, 1, 2)
    return fig
