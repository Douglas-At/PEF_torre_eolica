import plotly.graph_objs as go
from scipy.constants import g 
import numpy as np


class WindCalculator:
    def __init__(self,blade_length, tower_height,cd,wind_speed):
        self.blade_length = blade_length
        self.tower_height = tower_height
        self.wind_speed = wind_speed
        self.density = 3300
        self.cd = cd
        self.g = g
        self.raio = 2
    
        self.dict_diagrama = {"m":{"funcs":self.function_m,"color":"rgba(0, 0, 255, 0.3)","titulo":"Diagrama de Momentos Fletores (M)","unidade":"Nm"},
                              "v":{"funcs":self.function_v,"color":"rgba(0, 255, 0, 0.3)","titulo":"Diagrama de Forças Cortantes (V)","unidade":"N"},
                              "n":{"funcs":self.function_n,"color":"rgba(255, 0, 0, 0.3)","titulo":"Diagrama de Forças Normais (N)","unidade":"N"}}

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
            title='Turbina Eolica',
            xaxis=dict(title='Eixo X [m]', range=[-self.blade_length - 10, self.blade_length + 10], showgrid=False,scaleanchor='y',scaleratio=1),
            yaxis=dict(title='Altura [m]', range=[0, self.tower_height + self.blade_length + 10], showgrid=False),
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
        V = cd*g*A*v²(y-H)/2 # anexar resolução no papel 
        """
        return (self.cd*self.g* (self.raio * 2 * self.tower_height ) *self.wind_function()**2 * (y - self.tower_height)) / 2
    
    def function_n(self,y):
        """
        calculo de N no diagrama
        N = d*g*(y-H)
        """
        return self.density*self.g*(y-self.tower_height)

    def function_m(self,y):
        """
        calculo de m no diagrama
        m = cd*g*A*v²(H²/4 - Hy/2 + y²/4)
        """
        return self.cd * self.g * (self.raio * 2 * self.tower_height ) *self.wind_function()**2 * (self.tower_height**2 / 4 - self.tower_height * y / 2 + y**2 / 4)

    def plot_m(self):
        return self.generic_plot("m")
    
    def plot_n(self):
        return self.generic_plot("n")
    
    def plot_v(self):
        return self.generic_plot("v")

    def generic_plot(self,diagrama):
        y_values = np.linspace(0, self.tower_height, 500)
        m_values = [self.dict_diagrama[diagrama]["funcs"](y) for y in y_values]
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
            fillpattern=dict(shape='/', fgcolor=self.dict_diagrama[diagrama]["color"]),  
            mode='none'
        )

        layout = go.Layout(
            title=f'{self.dict_diagrama[diagrama]['titulo']}',
            xaxis=dict(
                title=f'{self.dict_diagrama[diagrama]['titulo']} [{self.dict_diagrama[diagrama]['unidade']}]',
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
