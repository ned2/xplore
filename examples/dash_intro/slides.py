import os

import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from xplore import Block
from xplore.layouts import *
from xplore.components import Col, Row


class Title(Block):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center']
    shape = [[6, 6]]
    row_classes = ['center-y']
    content = [
        html.Div(dcc.Markdown("""
#### Ned Letcher
    nedned.net
    @nletcher
"""), style={'text-align':'left'}),
        [
            Row(html.Img(src='/static/img/forefront.jpg',
                    style={'margin-bottom':'2em'})),
            Row(html.Img(src='/static/img/melbourne-uni.png',
                    style={'width':'35%'}))
        ]
    ]


class Context(Block):
    name = "The Problem"
    shape = [[8, 4]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(
"""
* You've done some analysis
* Want to communicate results with a visualisation
* It needs to be
    * _interactive_
    * _shareable_
"""),
        dcc.Markdown(
"""
But you have finite
* time
* people
* capabilities
""", className='warning note')
    ]


class JavaScript(Block):
    name = "JavaScript library?" 
    shape = [[8, 4]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(
"""
eg D3.js, plotly.js, Chart.js etc...
* but most data analytics not done in JavaScript
* integrating data will take time
* requires front-end development skills
* full stack developers??
"""),
        html.Div([
            Row(html.Img(src='/static/img/d3.png', style={'width':'30%'})),
            Row(html.Img(src='/static/img/plotly.png')),
            Row(html.Img(src='/static/img/chartjs.jpg')),
        ], className='center pad-y')
    ]


class R(Block):
    name = "R"
    shape = [[12]]
    classes = ['center']
    content = Row(html.Img(src='/static/img/shiny.png', style={'width':'50%'}))


class Python(Block):
    name = "Python"
    shape = [[9, 3]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(
"""
* **Jupyter**
    - Might already be using notebook for analysis
    - *But* can't expose kernel to the world
        - Notebook Server + Dashboard Server
        - *But* does not scale
* **Bokeh and Bokeh Server**
    - Good option
    - Some complexity involved?
* **Dash**...
"""),
        html.Div([
            Row(html.Img(src='/static/img/jupyter.svg', style={'width':'100%'})),
            Row(html.Img(src='/static/img/bokeh.png')),
            Row(html.Img(src='/static/img/dash.svg')),
        ], className='center pad-y')
    ]


class Dash(Block):
    shape = [[8, 4]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(
"""
* Python framework for building data-driven web applications
* Enables construction of modern reactive web-apps
    - __*Using just Python!!*__
* Built on
    - Flask (Python web framework)
    - React (JavaScript interface library)
"""),
        html.Div([
            Row(html.Img(src='/static/img/dash.svg', style={'width':'100%'})),
            Row(html.Img(src='/static/img/plotly.png')),
        ], className='center pad-y-extra')]


class DashExample(Block):
    name = "A Reactive Viz"
    shape = [
        [4, 8],
        [12]
    ]
    row_classes = ['center-y', '']

    def get_data(self):
        self.data = {}
        csv_path = os.path.join(self.project_path, 'data', 'indicators.csv.gz')
        self.data['df'] = pd.read_csv(os.path.join(csv_path))

    @property
    def content(self):
        df = self.data['df']
        available_indicators = df['Indicator Name'].unique()
        content = {
            'content-3': html.Div(dcc.Markdown(
"""
    function(input1, input2, input3, ...)  ==>  new_data
"""), className='center reveal', style={'font-size':'150%', 'margin-top':'2rem'}),
            'content-1':
            html.Div([
                Row(html.Div([
                    html.Div('y-axis', style={'opacity':0.7, 'margin-bottom':'0.25rem'}),
                    dcc.Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)'
                    ),
                    dcc.RadioItems(
                        id='yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={})),
                Row(html.Div([
                    html.Div('x-axis', style={'opacity':0.7, 'margin-bottom':'0.25rem'}),
                    dcc.Dropdown(
                        id='xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)'
                    ),
                    dcc.RadioItems(
                        id='xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={}))
            ], className='pad-y', style={'font-size':'x-large'}),
            'content-2' :
            html.Div([
                dcc.Graph(id='indicator-graphic'),
                dcc.Slider(
                    id='year--slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=df['Year'].max(),
                    step=None,
                    marks={str(year): str(year) for year in df['Year'].unique()}
                )
            ])
        }
        return content

    def callbacks(self, app):
        @app.callback(Output('indicator-graphic', 'figure'),
            [Input('xaxis-column', 'value'),
             Input('yaxis-column', 'value'),
             Input('xaxis-type', 'value'),
             Input('yaxis-type', 'value'),
             Input('year--slider', 'value')])
        def update_graph(xaxis_column_name, yaxis_column_name,
                         xaxis_type, yaxis_type,
                         year_value):
            df = self.data['df']
            dff = df[df['Year'] == year_value]

            return {
                'data': [go.Scatter(
                    x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                    y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                    text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
                    mode='markers',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    }
                )],
                'layout': go.Layout(
                    xaxis={
                        'title': xaxis_column_name,
                        'type': 'linear' if xaxis_type == 'Linear' else 'log'
                    },
                    yaxis={
                        'title': yaxis_column_name,
                        'type': 'linear' if yaxis_type == 'Linear' else 'log'
                    },
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                    hovermode='closest'
                )
            }


class Architecture(Block):
    name = "The Big Picture"
    shape = [[12]]
    classes = ['center']
    content = Row(html.Img(src='/static/img/dash-architecture.svg', style={'width':'70%'}))


class HelloWorld(Block):
    shape = [[6, 6]]
    row_classes = ['center-y']

    content = [
        dcc.SyntaxHighlighter(
"""
    data = np.random.normal(size=1000)

    app = dash.Dash()

    app.layout = html.Div([
        html.H2('Woah', style={'color':'red'}),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [data],
                'layout': {'title': 'Hello World'}
            }
        ),
        html.P('We made a thing!')
    ])
""", language='python'),
        html.Div(children=[
            html.H2('Woah', style={'color':'red'}),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [go.Histogram(x=np.random.normal(size=10000))],
                    'layout': {'title': 'Hello World'}
                }
            ),
            html.P('We made a thing!')

        ])
    ]


class Layouts(Block):
    shape = [[6, 2, 2, 2]]
    content = [
        dcc.Markdown(
"""
* *Reusable* Component trees
* Components are Python classes for
    * any HTML element
    * special Dash components (eg Graph)
* Converted to JSON and sent to browser
"""),
        html.Div(['Div',
             html.Ul([
                 html.Li('H2'),
                 html.Li('Graph'),
                 html.Li('P')
             ])
            ], className='clt'),
        html.Div(['Div',
             html.Ul([
                 html.Li('H1'),
                 html.Li(['Ul', html.Ul([html.Li('Li'), html.Li('Li'), html.Li('Li')])]),
             ])
            ], className='clt'),
        html.Div(['Div',
             html.Ul([
                 html.Li('Markdown'),
                 html.Li('Img'),
                 html.Li('Img')
             ])
            ], className='clt')
    ]


class ReactiveHelloWorld(Block):
    shape = [[6, 6]]
    row_classes = ['center-y']

    @property
    def content(self):
        content = [
            html.Div(dcc.SyntaxHighlighter(
"""
    app = dash.Dash()
    app.layout = html.Div([
                dcc.Graph(id='graph'),
                dcc.Slider(
                    id='slider',
                    min=0,
                    max=1001,
                    value=0,
                    step=100,
                    marks={i:i for i in
                           range(0, 1001, 100)}
                )
            ])

    @app.callback(
        Output('graph', 'figure'),
        [Input('slider', 'value')])
    def update_grapph(size):
        data = np.random.normal(size=size)
        return {'data': [go.Histogram(x=data)]}
""", language='python', customStyle={'padding':0}),
                style={'position':'relative', 'top':'-2em'}
            ),
            html.Div([
                dcc.Graph(id='graph'),
                dcc.Slider(
                    id='slider',
                    min=0,
                    max=1001,
                    value=0,
                    step=100,
                    marks={i:i for i in range(0, 1001, 100)}
                )
            ])
        ]
        return content

    def callbacks(self, app):

        @app.callback(Output('graph', 'figure'), [Input('slider', 'value')])
        def update_grapph(size):
            data = np.random.normal(size=size)
            return {'data': [go.Histogram(x=data)]}


class Callbacks(Block):
    shape = [[3, 9]]
    content = [[], html.Div(dcc.SyntaxHighlighter(
"""
    app = dash.Dash()
    app.layout = html.Div([
                dcc.Graph(id='graph'),
                dcc.Slider(
                    id='slider',
                    min=0,
                    max=1001,
                    value=0,
                    step=100,
                    marks={i:i for i in range(0, 1001, 100)}
                )
            ])

    @app.callback(Output('graph', 'figure'), [Input('slider', 'value')])
    def update_grapph(size):
        data = np.random.normal(size=size)
        return {'data': [go.Histogram(x=data)]}
""", language="python"), style={'position':'relative', 'top':'-1em'}
    )]

    # callback to change the data
    # maybe also a callback to insert an image.


# TODO: slides saying callbacks are for DOM also?


class LayoutsAndCallbacks(Block):
    name = "Layouts & Callbacks"
    shape = [[4, 8]]
    row_classes = ['center-y pad-top']
    content = [html.Div([
        html.Div(['Div',
             html.Ul([
                 html.Li('H2'),
                 html.Li('Graph'),
                 html.Li('P')
             ])
            ], className='clt')
    ], style={'margin-left':'3em'}),
               html.Div([
                   dcc.Markdown(
"""
function(input1, input2, ...)  ==>  Graph.figure
""")], className='center')]


    # just show the layout tree and the original function thing


class FeatureMarkdown(Block):
    name = "Markdown Component"
    shape = [[6, 6]]
    row_classes = [['center-y']]
    content = [
        dcc.SyntaxHighlighter(
'''
    app.layout = dcc.Markdown(
    """
    Markdown
    --------
    An easy to read and write **markup** language
    * automatically converted to HTML
    * makes inline content creation _much_ easier
    """)
''', language="python")
        ,
        dcc.Markdown(
"""
Markdown
--------
An easy to read and write **markup** language
* automatically converted to HTML
* makes inline content creation _much_ easier
""")]



class SinglePageApps(Block):
    shape = [[4, 8]]
    row_classes = [['center-y pad-top']]
    content = ['A simple URL router', dcc.SyntaxHighlighter(
"""
    app.callback(Output('main', 'children'), [Input('url', 'route')])
    def display_page(route):
        if route = '/':
            return home_layout
        elif route = '/viz1':
            return viz1_layout
        elif route = '/viz2':
            return viz2_layout
        else:
            return page_not_found_layout
""", language="python")]


class Extensible(Block):
    name = "Extensible Components"
    shape = [[12]]
    content = dcc.Markdown(
"""
* Dash layout components are React components
   - Can create custom own Dash layout components
   - existing React components can be converted to Dash components
   - Plotly has a toolchain for streamlining creation components  
   - Can be added to the open source Dash library for all to benefit
""")

    
class Deployment(Block):
    name = "Deploying on the cloud"
    shape = [[8, 4]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(
"""
* Dash/Flask comes with a built-in web server
    - only meant for development
    - can only handle one request at a time
* You need a WSGI server
    - Gunicorn
    - uWSGI
    - mod_wsgi (Apache)
* Will work on basically any hosting environment
    - potentially even Lambda (using Zappa)!!
"""),
        dcc.Markdown(
"""
Just Google:\\
"Hosting Flask apps on X"\\
Where X = AWS, Google Cloud, Azure, etc...
""", className='note center')
    ]



class Limitations(Block):
    shape = [[12]]
    content = dcc.Markdown(
"""
* Only supports plotly.js visualisations
    * but can create your own React components
* Every reactive event requires a web request
    * slower for remotely hosted apps
    * For layout changes can create React components
    * May be forthcoming features to help
""")


# TODO: why is last page being duplicated
class Conclusion(Block):
    name = "A Dashing Future"
    shape = [[12]]
    content = dcc.Markdown(
"""
* Dash enables creation interactive web apps in pure Python
    - designed for analytics applications
    - scalable
    - modern framework (without writing a line of JavaScript!)
* Teams can create reusable libraries of apps and layout components
* For
    - analysts
    - researchers
    - communicators
    - enthusiasts 
""")
