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
from xplore.components import Col, Row, Image, FontA, Box, BackgroundImage


# Time: 30 minutes

class Title(Block):
    name = "Front-end Web Development in Python using Dash"
    title = True
    shape = [[6, 6]]
    content = [
        html.Div(dcc.Markdown("""
#### Ned Letcher
    nedned.net
    @nletcher"""
        )),
        Image(src='forefront.png', width=90, style={'marginTop':'4em'})
    ]


class Context(Block):
    shape = [[6, 6], [12], [6, 6]]
    row_heights = [None, 20, None]
    content = [
        # TODO change this to tabular data: eg screen shot of dataframe in
        # jupyter notebook
        Image('code.jpg', round=True, width=65),
        Image('code.jpg', round=True, width=65),
        FontA('fa-arrow-down'),
        Image('charts.svg', round=True, width=65),
        Image('interfaces.jpg', round=True, width=65),
    ]


class Need(Block):
    name = "Needs to be"
    header = True
    content = html.Div(
        dcc.Markdown(
"""
* interactive
* sharable
* deployable
* scalable
"""), className="note")


class WebPlatform(Block):
    name = "The Web Platform"
    header = True
    content = Image('web.png', width=80)


class Madness(Block):
    content = BackgroundImage(src='js_madness.png')


class Glue(Block):
    content = BackgroundImage(src='switchboard.jpg')


class WeWant(Block):
    header = True
    shape = [[6]]
    content = Box(dcc.Markdown(
"""
A simple framework for developing interactive web applications *within* Python 
"""), center=True)


class Dash(Block):
    shape = [
        [12],
        [12],
        [4, 8]
    ]
    row_heights = [None, 15, None]
    content = [
        Image(src='dash.svg', width=50),
        html.Div(),
        html.Div([
            Row(Image(src='flask.png', width=50), hcenter=True),
            Row(Image(src='react.png', width=50), hcenter=True),
            Row(Image(src='plotly.png', width=50), hcenter=True),
        ]),
        dcc.Markdown(
"""
* Framework for building data-driven reactive web applications __*using only Python!!*__
* Made by Plotly
* Open source (MIT Licence)
* Active community
* ~3k ★ on GitHub
""")
        ]


class DashExample(Block):
    name = "A Reactive Dash App"
    header = True
    hcenter = False
    vcenter = False
    shape = [
        [12],
        [4, 8]
    ]
    row_heights = [10, None]
    
    def get_data(self):
        self.data = {}
        csv_path = os.path.join(self.project_path, 'data', 'indicators.csv.gz')
        self.data['df'] = pd.read_csv(os.path.join(csv_path))

    @property
    def content(self):
        df = self.data['df']
        available_indicators = df['Indicator Name'].unique()
        content = {
            'content-1': html.Div(),
            'content-2':
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
            'content-3' :
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


class DashArchitecture(Block):
    header = True
    content = Image(src='dash-architecture.svg', width='80vw')


class HelloWorld(Block):
    header = True
    shape = [
        [None],
        [None, None]
    ]
    row_heights = [5, None]
    hcenter = False
    vcenter = False
    
    content = [
        html.Div(),
        html.Div(
            children=dcc.SyntaxHighlighter(
                language='python',
                theme='dark',           
                children="""
app = dash.Dash()
data = np.random.normal(size=1000)

app.layout = html.Div(
    className="center",
    children=[
        html.H2('Woah', style={'color':'red'}),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [go.Histogram(x=data)],
                'layout': {'title': 'Hello World'}
            }
        ),
        html.P('We made a thing!')
    ]
)
""".strip()
            )
        ),
        html.Div(
            style={'textAlign':'center'},
            children=[
                html.H2('Woah', style={'color':'red'}),
                dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [go.Histogram(x=np.random.normal(size=10000))],
                        'layout': {'title': 'Hello World'}
                    }
                ),
                html.P('We made a thing!')           
            ]
        )
    ]


class ReactiveHelloWorld(Block):
    shape = [
        [None],
        [None, None]
    ]
    row_heights = [5, None]
    header = True
    hcenter = False
    vcenter = False

    @property
    def content(self):
        content = [
            html.Div(),
            html.Div(dcc.SyntaxHighlighter(
                theme='dark',
                language='python', 
                children="""
app = dash.Dash()
app.layout = html.Div(
    children=[                
        dcc.Graph(id='graph'),
        dcc.Slider(
            id='slider',
            min=0,
            max=1001,
            value=0,
            step=100,
            marks={i:i for i in range(0, 1001, 100)}
        )
    ]
)

@app.callback(
    Output('graph', 'figure'),
    [Input('slider', 'value')])
def update_grapph(size):
    data = np.random.normal(size=size)
    return {'data': [go.Histogram(x=data)]}
""".strip()
            )),
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


# create image with markup
class UnpackingThings(Block):
    header = True
    shape = [[3, 9]]
    content = [
        html.Div(),
        html.Div(dcc.SyntaxHighlighter(
            theme='dark',
            language='python', 
            children="""
app = dash.Dash()
app.layout = html.Div(
    children=[                
        dcc.Graph(id='graph'),
        dcc.Slider(
            id='slider',
            min=0,
            max=1001,
            value=0,
            step=100,
            marks={i:i for i in range(0, 1001, 100)}
        )
    ]
)

@app.callback(Output('graph', 'figure'), [Input('slider', 'value')])
def update_grapph(size):
    data = np.random.normal(size=size)
    return {'data': [go.Histogram(x=data)]}
""".strip()))
]

        
class Layouts(Block):
    header = True    
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


class LayoutsAndCallbacks(Block):
    Name = "Layouts and Callbacks"
    title = True


class FeatureMarkdown(Block):
    name = "Markdown Component"
    shape = [[6, 6]]
    row_classes = ['center-y']
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

    
# Add:
# -- can only target one output element
# -- each element-property pair can only be the output of one callback
    
class Callbacks(Block):
    header = True



    # callback to change the data
    # maybe also a callback to insert an image.


# TODO: slides saying callbacks are for DOM also?


class SinglePageApps(Block):
    shape = [[4, 8]]
    row_classes = ['center-y pad-top']
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
