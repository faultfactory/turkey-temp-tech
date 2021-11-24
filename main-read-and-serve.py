#!/usr/bin/env python3
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
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


app = dash.Dash(__name__)

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
	html.H3(children="FriendsgivingTech Advanced Development Group"),
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='Thigh Temperature - High Speed Trace'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph1',
				animate = True
            ),
			dcc.Interval(
			id = 'fast-update',
			interval = 1000,
			n_intervals = 0
		)  
        ], className='six columns'),
        html.Div([
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for Python.
            '''),

            dcc.Graph(
                id='graph2',
				animate = True
            ),  
        ], className='six columns'),
    ], className='row'),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='graph3',
			animate = True
        ),
		  
    ], className='row'),
])

@app.callback(
	Output('thigh-graph', 'figure'),
	[ Input('slow-update', 'n_intervals') ]
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
