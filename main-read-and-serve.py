#!/usr/bin/env python3
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import dash_daq as daq
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen = 600)
X.append(1)

Y = deque(maxlen = 600)
Y.append(1)

lowSpeed_thigh = deque(maxlen = 600)
lowSpeed_breast = deque(maxlen = 600)

highSpeed_thigh = deque(maxlen = 600)
highSpeed_breast = deque(maxlen = 600)

lowSpeedIntervalMS = 5000
highSpeedIntervalMS = 200


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
	html.H6(children="Oh boy!"),
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H4(children='Thigh Temperature - High Speed Trace'),
            html.Div([
            daq.Thermometer(
                min=50,
                max=200,
                value=100,
                height=400,
                showCurrentValue=True,
                units="F",
            )], style={'vertical_align': 'center'},className='one column'), 
            html.Div([
            dcc.Graph(
                id='thigh-graph',
				animate = True,
            ),
			dcc.Interval(
			id = 'thigh_fast',
			interval = 1000,
			n_intervals = 0
            ), 
            ], )
        ],  className='six columns'),

        html.Div([
            html.H4(children='Breast Temperature - High Speed Trace'),
            html.Div([
            daq.Thermometer(
                min=50,
                max=200,
                value=100,
                height=400,
                showCurrentValue=True,
                units="F",
            )], style={'vertical_align': 'center'},className='one column'), 
            html.Div([
            dcc.Graph(
                id='breast-graph',
				animate = True,
            ),
			dcc.Interval(
			id = 'breast_fast',
			interval = 1000,
			n_intervals = 0
            ), 
            ], )
        ],  className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H4(children='Long Term Temperature Trend for Turkey'),
        dcc.Graph(
            id='long-term',
			animate = True
        ),
		  
    ], className='row'),
])

@app.callback(
	Output('thigh-graph', 'figure'),
	[ Input('thigh_fast', 'n_intervals') ],
    Output('breast-graph', 'figure'),
	[ Input('breast_fast', 'n_intervals') ]
)

def update_graph_scatter(n):
	X.append(X[-1]+1)
	Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))

	data = plotly.graph_objs.Scatter(
			x=list(X),
			y=list(Y),
			name='Scatter',
			mode= 'lines+markers'
	)

	return {'data': [data],
			'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}

if __name__ == '__main__':
	app.run_server(host= '0.0.0.0',debug=False)
