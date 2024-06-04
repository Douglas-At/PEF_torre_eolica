
import plotly.graph_objs as go
import numpy as np


class WindCalculator:
    def __init__(self,blade_length, tower_height):
        self.blade_length = blade_length
        self.tower_height = tower_height

    def wind_function(self,y):
        return np.log(y + 1) * 2  

    def plot_turbine(self):
        angles = np.linspace(0, 2 * np.pi, 4)[:-1]
        x_blades = [self.blade_length * np.cos(angle) for angle in angles]
        y_blades = [self.tower_height + self.blade_length * np.sin(angle) for angle in angles]

        traces = [
            go.Scatter(x=[0, 0], y=[0, self.tower_height], mode='lines', line=dict(color='black', width=5), name='Tower'),
        ]

        for x, y in zip(x_blades, y_blades):
            traces.append(go.Scatter(x=[0, x], y=[self.tower_height, y], mode='lines', line=dict(color='blue', width=2), name='Blade'))

        layout = go.Layout(
            title='Wind Turbine',
            xaxis=dict(title='X axis', range=[-self.blade_length - 10, self.blade_length + 10], showgrid=False),
            yaxis=dict(title='Y axis', range=[0, self.tower_height + self.blade_length + 10], showgrid=False),
            showlegend=False,
            height=600
        )

        return {'data': traces, 'layout': layout}

    def plot_wind_behavior(self):
        y_values = np.linspace(0, self.tower_height + self.blade_length, 500)
        wind_speeds = self.wind_function(y_values)

        trace = go.Scatter(x=wind_speeds, y=y_values, mode='lines', line=dict(color='green'))

        layout = go.Layout(
            title='Wind Speed vs. Height',
            xaxis=dict(title='Wind Speed'),
            yaxis=dict(title='Height'),
            height=600
        )

        return {'data': [trace], 'layout': layout}