from plotly import tools

def y_actual(x, x_values, y_values):
    combined_values = list(zip(x_values, y_values))
    point_at_x = list(filter(lambda point: point[0] == x,combined_values))[0]
    return point_at_x[1]

def error(x_values, y_values, m, b, x):
    expected = (m*x + b)
    return (y_actual(x, x_values, y_values) - expected)


def error_line_trace(x, y, error):
    name = 'error at ' + str(x)
    return {'x': [x, x], 'y': [y - error, y], 'mode': 'lines', 'marker': {'color': 'red'}, 'name': name, 'text': [error], 'textposition':'top right', 'hoverinfo': 'none'}

def error_line_traces(x_values, y_values, errors):
    coords_and_errors = list(zip(x_values, y_values, errors))
    return [error_line_trace(coords_and_error[0], coords_and_error[1], coords_and_error[2]) for coords_and_error in coords_and_errors]

def errors_from_model(m, b, x_values, y_values):
    y_hats = list(map(lambda x: m*x + b, x_values))
    y_values_y_hats = list(zip(y_values, y_hats))
    errors = list(map(lambda pair: pair[0] - pair[1], y_values_y_hats))
    return error_line_traces(x_values, y_values, errors)




def squared_error(x_values, y_values, m, b, x):
    return error(x_values, y_values, m, b, x)**2

def squared_errors(x_values, y_values, m, b):
    return list(map(lambda x: squared_error(x_values, y_values, m, b, x), x_values))

def residual_sum_squares(x_values, y_values, m, b):
    return round(sum(squared_errors(x_values, y_values, m, b)), 2)

def error_from_parameters(m, b, x, y):
    y_hat = m*x + b 
    return y - y_hat

def rss(m, b, x_values, y_values):
    squared_errors = []
    pairs = list(zip(x_values, y_values))
    for pair in pairs:
        squared_error = error_from_parameters(m, b, pair[0], pair[1])**2
        squared_errors.append(squared_error)
    return sum(squared_errors)


def bar_chart(y_value, name= ''):
    rss_calc = residual_sum_squares(x_values, y_values, m, b)
    return dict(
        x=[name],
        y=[y_value],
        type='bar'
    )

def trace_rss(x_values, y_values, m, b):
    rss_calc = residual_sum_squares(x_values, y_values, m, b)
    return dict(
        x=['RSS'],
        y=[rss_calc],
        type='bar'
    )

def plot_regression_and_rss(scatter_trace, regression_trace, rss_calc_trace):
    fig = tools.make_subplots(rows=1, cols=2)
    fig.append_trace(scatter_trace, 1, 1)
    fig.append_trace(regression_trace, 1, 1)
    fig.append_trace(rss_calc_trace, 1, 2)
    plotly.offline.iplot(fig)
