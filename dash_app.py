import dash_app
from dash_app import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from wind_tower import WindCalculator

app = dash_app.Dash(__name__)



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
    wc = WindCalculator(blade_length,tower_height)
    turbine_fig = wc.plot_turbine(blade_length, tower_height)
    wind_fig = wc.plot_wind_behavior(tower_height, blade_length)
    return turbine_fig, wind_fig

if __name__ == '__main__':
    app.run_server(debug=True)
