from graph import trace_values, plot
from graph import m_b_trace, plot, m_b_data, trace_values
from error import error_line_traces
import plotly.plotly as py
angles = [.1, .2, .3, .4, .5, .6, .7]
predicted_distances = list(map(lambda angle: 40 * angle, angles))
data_trace = trace_values([.30, .50, .70], [8, 11, 17], name = 'actual shots')
observed_shot_angles = [.30, .50, .70]
observed_distances =     [8, 11, 17]
    
def plot_data_and_model():
    model_trace = trace_values(angles, predicted_distances, mode = 'lines', name = 'model')
    layout = {'yaxis': {'range': [0, 18], 'title': 'shot distance'}, 'xaxis': {'title': 'shot angle'}}
    return py.plot([data_trace, model_trace])


def plot_data_and_errors():
    inputs = [.30, .40, .50, .60, .70]
    predictions = list(map(lambda angle: 40*angle,inputs))
    predictions_trace = trace_values(inputs, predictions, 'lines', name = 'predictions')
    errors = [-4, -9, -11]
    error_traces = error_line_traces(observed_shot_angles, observed_distances, errors)
    return py.plot([data_trace, predictions_trace] + error_traces)


def updated_model_with_errors(parameter):
    layout = {'yaxis': {'range': [0, 18], 'title': 'shot distance'}, 'xaxis': {'title': 'shot angle'}}
    predictions = list(map(lambda angle: parameter*angle, observed_shot_angles))
    actual_trace = trace_values(observed_shot_angles, observed_distances, name = 'actual shots')
    predictions_trace = trace_values(observed_shot_angles, predictions, 'lines', name = 'predictions')
    y_values_y_hats = list(zip(observed_distances, predictions))
    errors = list(map(lambda pair: pair[0] - pair[1], y_values_y_hats))
    error_traces = error_line_traces(observed_shot_angles, observed_distances, errors)
    return py.plot([actual_trace, predictions_trace] + error_traces)