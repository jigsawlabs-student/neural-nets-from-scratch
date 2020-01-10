import plotly.graph_objects as go

def slope_at(point_one, point_two):
    return (point_two[1] - point_one[1])/((point_two[0] - point_one[0]))

def slope_trace(point_one, point_two):
    slope = slope_at(point_one, point_two)
    distance = 1*(point_two[0] - point_one[0])
    start_x =  point_one[0] - distance
    end_x  = point_one[0] + distance
    start_y = point_one[1] - slope*distance 
    end_y = point_one[1] + slope*distance
    slope_text = str(int(slope))
    return go.Scatter(x=[start_x, end_x], y=[start_y, end_y], name = 'slope = ' + slope_text)
