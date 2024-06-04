import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from wind_tower import WindCalculator

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Label('Tamanho das Pás [m]'),
        dcc.Slider(id='blade-slider',min=5,max=30,step=1,value=15,marks={i: str(i) for i in range(5, 31)}),
        html.Label('Altura da Torre [m]'),
        dcc.Slider(id='tower-slider',min=20,max=200,step=10,value=70,marks={i: str(i) for i in range(20, 201, 10)}),
        html.Div([
            dcc.Graph(id='turbine-plot'),
            dcc.Graph(id='wind-plot'),
        ]),
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        html.H3('Diagramas de Esforços na Torre', style={'textAlign': 'center'}),
        dcc.Graph(id='n-plot'),
        dcc.Graph(id='v-plot'),
        dcc.Graph(id='m-plot'),
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
], style={'display': 'flex', 'flex-direction': 'row'})



@app.callback(
    [Output('turbine-plot', 'figure'),
     Output('wind-plot', 'figure'),
     Output('n-plot', 'figure'),
     Output('v-plot', 'figure'),
     Output('m-plot', 'figure')],
    [Input('blade-slider', 'value'),
     Input('tower-slider', 'value')]
)
def update_plots(blade_length, tower_height):
    
    wc = WindCalculator(blade_length=blade_length,tower_height=tower_height, cd=0.82,wind_speed=10)
    turbine_fig = wc.plot_turbine()
    wind_fig = wc.plot_wind_behavior()
    n_fig = wc.plot_n()  
    v_fig = wc.plot_v() 
    m_fig = wc.plot_m()
    
    return turbine_fig, wind_fig, n_fig, v_fig, m_fig

if __name__ == '__main__':
    app.run_server(debug=True)
