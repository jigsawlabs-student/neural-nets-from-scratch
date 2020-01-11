from graph import trace_values, plot
from graph import m_b_trace, plot, m_b_data, trace_values
from error import error_line_traces

angles = [.1, .2, .3, .4, .5, .6, .7]
predicted_distances = list(map(lambda angle: 40 * angle, angles))
model_trace = trace_values(angles, predicted_distances, mode = 'lines', name = 'model')
data_trace = trace_values([2000, 3500, 4000], [260, 445, 490], name = 'actual sales')
observed_ad_spends = [2000, 3500, 4000]
observed_sales = [260, 445, 490]
    
def plot_data_and_model():
    inputs = list(range(1500, 4500, 250))
    predictions = list(map(lambda input: .15*input,inputs))
    predictions_trace = trace_values(inputs, predictions, 'lines', name = 'predictions')
    data_trace = trace_values([2000, 3500, 4000], [260, 445, 490], name = 'actual sales')
    layout = {'yaxis': {'range': [0, 18], 'title': 'sales'}, 'xaxis': {'title': 'ad spend'}}
    return plot([data_trace, predictions_trace])


def plot_data_trace():
    return plot([data_trace])
def plot_data_and_errors():
    inputs = list(range(1500, 4500, 250))
    predictions = list(map(lambda input: .15*input,inputs))
    predictions_trace = trace_values(inputs, predictions, 'lines', name = 'predictions')
    errors = [-40, -80, -110]
    ad_spends = [2000, 3500, 4000]
    sales = [260, 445, 490]
    error_traces = error_line_traces(ad_spends, sales, errors)
    return plot([data_trace, predictions_trace] + error_traces)

def updated_model_with_errors(parameter):
    layout = {'yaxis': {'range': [0, 450], 'title': 'sales'}, 'xaxis': {'title': 'ad spend'}}
    inputs = list(range(1500, 4500, 250))
    
    predictions = list(map(lambda ad_spend: parameter*ad_spend, observed_ad_spends))
    data_trace = trace_values([2000, 3500, 4000], [260, 445, 490], name = 'actual sales')
    predictions_trace = trace_values(observed_ad_spends, predictions, 'lines', name = 'predictions')
    y_values_y_hats = list(zip(observed_sales, predictions))
    errors = list(map(lambda pair: pair[0] - pair[1], y_values_y_hats))
    error_traces = error_line_traces(observed_ad_spends, observed_sales, errors)
    return plot([data_trace, predictions_trace] + error_traces)