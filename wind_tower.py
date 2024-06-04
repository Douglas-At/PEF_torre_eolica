import plotly.graph_objs as go
from scipy.constants import g 
import numpy as np


class WindCalculator:
    def __init__(self,blade_length, tower_height,cd,wind_speed):
        self.blade_length = blade_length
        self.tower_height = tower_height
        self.wind_speed = wind_speed
        self.cd = cd
        self.g = g

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
    
    def wind_function(self):
        return self.wind_speed

    def plot_wind_behavior(self):
        y_values = np.linspace(0, self.tower_height + self.blade_length, 500)
        
        wind_speeds = np.full_like(y_values, self.wind_function())
        

        trace = go.Scatter(x=wind_speeds, y=y_values, mode='lines', line=dict(color='green'))

        layout = go.Layout(
            title='Velocida do Vento x Altura',
            xaxis=dict(title='Velocidade do Vento [m/s]'),
            yaxis=dict(title='Altura [m]'),
            height=600
        )
        
        return {'data': [trace], 'layout': layout}
    
    def function_v(self,y):
        """
        calculo de v no diagrama
        V = cd*g*v²(y-H)/2 # anexar resolução no papel 
        """
        return (self.cd*self.g*self.wind_function()**2 * (y - self.tower_height)) / 2

    def plot_v(self):
        y_values = np.linspace(0, self.tower_height, 500)
        v_values = [self.function_v(y) for y in y_values]
        max_abs_v = max(abs(min(v_values)), abs(max(v_values)))

        traces = [go.Scatter(x=[0, 0], y=[0, self.tower_height], mode='lines', line=dict(color='black', width=5), name='Tower')]
        traces.append(go.Scatter(x=v_values, y=y_values, mode='lines', line=dict(color='red')))

        filled_area = go.Scatter(x=v_values + [0],y=y_values.tolist() + [y_values[0]],fill='tozerox',
                                 fillpattern=dict(shape='\\'),mode='none' ,fillcolor='rgba(255, 0, 0, 0.3)')

        layout = go.Layout(
            title='Diagrama de Forças Cortantes (V)',
            xaxis=dict(title='Força Cortante (V) [N]',showgrid=True,gridcolor='lightgrey',range=[-max_abs_v, max_abs_v]),
            yaxis=dict(title='Altura [m]'),
            height=600,
            showlegend=False
        )

        return {'data': [filled_area] + traces, 'layout': layout}

    def function_m(self,y):
        """
        calculo de m no diagrama
        m = cd*g*v²(H²/4 - Hy/2 + y²/4)
        """
        return self.cd * self.g * self.wind_function()**2 * (self.tower_height**2 / 4 - self.tower_height * y / 2 + y**2 / 4)


    def plot_m(self):
        y_values = np.linspace(0, self.tower_height, 500)
        m_values = [self.function_m(y) for y in y_values]
        max_abs_m = max(abs(min(m_values)), abs(max(m_values)))

        traces = [
            # o poste
            go.Scatter(x=[0, 0], y=[0, self.tower_height], mode='lines', line=dict(color='black', width=5), name='Tower'),
            go.Scatter(x=m_values, y=y_values, mode='lines', line=dict(color='blue'))
        ]

        
        filled_area = go.Scatter(
            x=m_values + [0],
            y=y_values.tolist() + [y_values[0]],
            fill='tozerox',
            fillpattern=dict(shape='/', fgcolor='rgba(0, 0, 255, 0.3)'),  
            mode='none'
        )

        layout = go.Layout(
            title='Diagrama de Momentos Fletores (M)',
            xaxis=dict(
                title='Diagrama de Momentos Fletores (M) [Nm]',
                showgrid=True,
                gridcolor='lightgrey',
                range=[-max_abs_m, max_abs_m]
            ),
            yaxis=dict(
                title='Altura [m]'
            ),
            height=600,
            showlegend=False
        )

        return {'data': [filled_area] + traces, 'layout': layout}


