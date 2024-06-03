import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

app = dash.Dash(__name__)

def wind_function(y):
    return np.cos(y / 20) * 10

def plot_turbine(blade_length, tower_height):
    angles = np.linspace(0, 2 * np.pi, 4)[:-1]
    x_blades = [blade_length * np.cos(angle) for angle in angles]
    y_blades = [tower_height + blade_length * np.sin(angle) for angle in angles]

    traces = [
        go.Scatter(x=[0, 0], y=[0, tower_height], mode='lines', line=dict(color='black', width=5), name='Tower'),
    ]

    for x, y in zip(x_blades, y_blades):
        traces.append(go.Scatter(x=[0, x], y=[tower_height, y], mode='lines', line=dict(color='blue', width=2), name='Blade'))

    layout = go.Layout(
        title='Wind Turbine',
        xaxis=dict(title='X axis', range=[-blade_length - 10, blade_length + 10], showgrid=False),
        yaxis=dict(title='Y axis', range=[0, tower_height + blade_length + 10], showgrid=False),
        showlegend=False,
        height=600
    )

    return {'data': traces, 'layout': layout}

def plot_wind_behavior(tower_height, blade_length):
    y_values = np.linspace(0, tower_height + blade_length, 500)
    wind_speeds = wind_function(y_values)

    trace = go.Scatter(x=wind_speeds, y=y_values, mode='lines', line=dict(color='green'))

    layout = go.Layout(
        title='Wind Speed vs. Height',
        xaxis=dict(title='Wind Speed'),
        yaxis=dict(title='Height'),
        height=600
    )

    return {'data': [trace], 'layout': layout}

app.layout = html.Div([
    html.Div([
        html.Label('Blade Length'),
        dcc.Slider(
            id='blade-slider',
            min=5,
            max=30,
            step=1,
            value=15,
            marks={i: str(i) for i in range(5, 31)}
        ),
        html.Label('Tower Height'),
        dcc.Slider(
            id='tower-slider',
            min=20,
            max=100,
            step=5,
            value=70,
            marks={i: str(i) for i in range(20, 101, 5)}
        ),
    ], style={'margin-bottom': '20px'}),
    html.Div([
        dcc.Graph(id='turbine-plot'),
        dcc.Graph(id='wind-plot'),
    ]),
])

@app.callback(
    [Output('turbine-plot', 'figure'),
     Output('wind-plot', 'figure')],
    [Input('blade-slider', 'value'),
     Input('tower-slider', 'value')]
)
def update_plots(blade_length, tower_height):
    turbine_fig = plot_turbine(blade_length, tower_height)
    wind_fig = plot_wind_behavior(tower_height, blade_length)
    return turbine_fig, wind_fig

if __name__ == '__main__':
    app.run_server(debug=True)
