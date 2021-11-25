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
import pandas as pd


lowSpeed_thigh = deque(maxlen = 600)
lowSpeed_breast = deque(maxlen = 600)
lowSpeed_timeline = deque(maxlen = 600)

highSpeed_thigh = deque(maxlen = 30)
highSpeed_breast = deque(maxlen = 30)
highSpeed_timeline= deque(maxlen = 30)

lowSpeedIntervalMultiplier = 10
highSpeedIntervalMS = 1000

def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div(
# 	[	html.Label('Thigh'),
# 		dcc.Graph(id = 'thigh-graph', animate = True),
# 		dcc.Interval(
# 			id = 'slow-update',
# 			interval = 1000,
# 			n_intervals = 0
# 		)
# 	],
# 	[ 	html.Label('Breast'),
# 		dcc.Graph(id = 'breast-graph', animate = True),
		# dcc.Interval(
		# 	id = 'fast-update',
		# 	interval = 1000,
		# 	n_intervals = 0
		# )
# 	]
# )

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
    offlineDebug = True
    updateSlow = n%lowSpeedIntervalMultiplier==0   

    if offlineDebug:
        highSpeed_thigh.append(1+random.uniform(-0.1,0.1))
        highSpeed_breast.append(1+random.uniform(-0.1,0.1))
        highSpeed_timeline.append(datetime.now())
        if(updateSlow):
            lowSpeed_breast.append(highSpeed_breast[-1])
            lowSpeed_thigh.append(highSpeed_thigh[-1])
            lowSpeed_timeline.append(highSpeed_timeline[-1])



    thigh_fig = go.Figure(data=go.Scatter(
        x=list(highSpeed_timeline),
        y=list(highSpeed_thigh),
        name='Scatter',
        mode= 'lines+markers'))
    thigh_fig.layout =  go.Layout(
                xaxis=dict(range=[min(highSpeed_timeline),max(highSpeed_timeline)]),
                yaxis = dict(range = [min(highSpeed_thigh),max(highSpeed_thigh)]),)

    breast_fig  =go.Figure(data=go.Scatter(
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

    # df = pd.DataFrame({'Time': lowSpeed_timeline,
    #      'Thigh':lowSpeed_thigh,
    #      'Breast': lowSpeed_breast})
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
	app.run_server(host= '0.0.0.0',debug=True)
