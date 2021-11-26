#!/usr/bin/env python3
from datetime import datetime
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import dash_daq as daq
import plotly
import random
import plotly.graph_objects as go
from collections import deque
from mcp9600 import MCP9600 
import threading
import time


highSpeed_thigh = deque(maxlen = 30)
highSpeed_breast = deque(maxlen = 30)
highSpeed_timeline= deque(maxlen = 30)

lowSpeed_thigh = deque(maxlen = 600)
lowSpeed_breast = deque(maxlen = 600)
lowSpeed_timeline = deque(maxlen = 600)

lowSpeedIntervalMultiplier = 10
highSpeedIntervalMS = 1000
offlineDebug = False

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def fahrenheit(temp_in_celcius):
    return (temp_in_celcius*9.0/5.0 + 32.0)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


class DashThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name


    def run(self):
        global app
        global highSpeed_thigh
        global highSpeed_breast
        global highSpeed_timeline
        global lowSpeed_breast
        global lowSpeed_thigh
        global lowSpeed_timeline
        app.layout = html.Div(
            [html.H1(children='Turkey Vision 3000'),
            # All elements from the top of the page
            html.Div([
                html.Div([
                    dcc.Interval(
                    id = 'fast',
                    interval = highSpeedIntervalMS,
                    n_intervals = 0
                    ), 
                    html.H4(children='Thigh Temperature'),
                    html.Div([
                    daq.LEDDisplay(
                        id='thigh_indicator',
                        label=" ",
                        value=6,
                        color="#FF0000",
                        size=60
                        ),
                    dcc.Graph(
                        id='thigh-graph',
                        animate = True,
                    ),],)
                ],  className='six columns'),
                html.Div([
                    html.H4(children='Breast Temperature'),
                    html.Div([
                    daq.LEDDisplay(
                        id='breast_indicator',
                        label=" ",
                        value=6,
                        color="#FF0000",
                        size=60
                        ),
                    dcc.Graph(
                        id='breast-graph',
                        animate = True,
                    ),], )
                ],  className='six columns'),
            ], style={'display': 'flex', 'flex-direction': 'row'}),
            # New Div for all elements in the new 'row' of the page
            html.Div([
                html.H4(children='Long Term Temperature Trend for Turkey'),
                dcc.Interval(
                    id = 'slow',
                    interval = highSpeedIntervalMS*lowSpeedIntervalMultiplier,
                    n_intervals = 0
                    ), 
                dcc.Graph(
                    id='long-term',
                    animate = True
                ),
                
            ], className='row'),
        ])

            
        @app.callback([
            Output('thigh-graph', 'figure'),
            Output('breast-graph', 'figure'),
            Output('thigh_indicator', 'value'),
            Output('breast_indicator', 'value')],[
            Input('fast', 'n_intervals')])
        def update_fast_elements(n):
            thigh_fig = go.Figure(data=go.Scatter(
                x=list(highSpeed_timeline),
                y=list(highSpeed_thigh),
                name='Scatter',
                mode= 'lines+markers'))
            thigh_fig.layout= go.Layout(
                        xaxis=dict(range=[min(highSpeed_timeline),max(highSpeed_timeline)]),
                        yaxis = dict(range = [min(highSpeed_thigh),max(highSpeed_thigh)]),)

            breast_fig =go.Figure(data=go.Scatter(
                x=list(highSpeed_timeline),
                y=list(highSpeed_breast),
                name='Scatter',
                mode= 'lines+markers'))
            breast_fig.layout = go.Layout(
                xaxis=dict(range=[min(highSpeed_timeline),max(highSpeed_timeline)]),
                yaxis = dict(range = [min(highSpeed_breast),max(highSpeed_breast)]),)
            
            return thigh_fig,breast_fig,truncate(highSpeed_thigh[-1],2),truncate(highSpeed_breast[-1],2)


        @app.callback(
            Output('long-term', 'figure'),
            Input('slow', 'n_intervals'))
        def update_slow_elements(n):
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(lowSpeed_timeline),
                y=list(lowSpeed_thigh),
                name='Thigh',
                mode= 'lines+markers',
                showlegend=True))
            fig.add_trace(go.Scatter(
                x=list(lowSpeed_timeline),
                y=list(lowSpeed_breast),
                name='Breast',
                mode= 'lines+markers',
                showlegend=True)),
            fig.layout = go.Layout(xaxis=dict(range=[min(lowSpeed_timeline),max(lowSpeed_timeline)]),yaxis = dict(range = [min(min(lowSpeed_thigh),min(lowSpeed_breast)),max(max(lowSpeed_thigh),max(lowSpeed_breast))]),)
            return fig

        #def update_total_slow(n);

        if __name__ == '__main__':
            app.run_server(host= '0.0.0.0',debug=False)




class ThermoCoupleThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = 0
        if not offlineDebug:
            self.thighProbe = MCP9600(i2c_addr=0x66)
            self.thighProbe.set_thermocouple_type('K')
            self.breastProbe = MCP9600(i2c_addr=0x60)
            self.breastProbe.set_thermocouple_type('K')   


    def run(self):
        global offlineDebug
        global highSpeed_thigh
        global highSpeed_breast
        global highSpeed_timeline
        global lowSpeed_timeline
        global lowSpeed_thigh
        global lowSpeed_breast
        while True:
            if offlineDebug:
                highSpeed_thigh.append(1+random.uniform(-0.1,0.1))
                highSpeed_breast.append(1+random.uniform(-0.1,0.1))
                highSpeed_timeline.append(datetime.now())
            else:
                highSpeed_thigh.append(fahrenheit(self.thighProbe.get_hot_junction_temperature()))
                highSpeed_breast.append(fahrenheit(self.breastProbe.get_hot_junction_temperature()))
                highSpeed_timeline.append(datetime.now())
            
            # updateSlow = counter%lowSpeedIntervalMultiplier==0   
            # if(updateSlow):
            lowSpeed_breast.append(highSpeed_breast[-1])
            lowSpeed_thigh.append(highSpeed_thigh[-1])
            lowSpeed_timeline.append(highSpeed_timeline[-1])
            
            counter+=1
            time.sleep(1)


a = DashThread("The Dash Application")
b = ThermoCoupleThread("An Independent Thread")

b.start()
a.start()

a.join()
b.join()




