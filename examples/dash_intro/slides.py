import os

import pandas as pd
import numpy
import dash
import plotly.graph_objs as go
from dash_html_components import *
from dash_core_components import *


from xplore import Block
from xplore.layouts import *


class Title(Block):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center']
    shape = [[6, 6]]
    row_classes = [['center-y']]
    content = [
        #one_col_row(Div(style={'height':'1em'})),
        Div(Markdown(
"""
#### Ned Letcher
    nedned.net
    @nletcher
"""), style={'text-align':'left'}),
        [
            one_col_row(Img(src='/static/img/forefront.jpg',
                            style={'margin-bottom':'2em'})),
            one_col_row(Img(src='/static/img/melbourne-uni.png',
                            style={'width':'35%'}))
        ]
    ]

    
class Context(Block):
    name = "So you have some data" 
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [
        Markdown(
"""
* You've done some analysis
* You want to communicate results with a visualisation
* It needs to be
    * _interactive_
    * _shareable_
"""),
        Markdown(
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
    row_classes = [['center-y']]
    content = [
        Markdown(
"""
eg D3.js, plotly.js, Chart.js etc...
* but most data analytics not done in JavaScript
* integrating data will take time
* requires front-end development skills
* full stack developers??
"""),
        Div([
            one_col_row(Img(src='/static/img/d3.png', style={'width':'30%'})),
            one_col_row(Img(src='/static/img/plotly.png')),
            one_col_row(Img(src='/static/img/chartjs.jpg')),
        ], className='center pad-y')
    ]
    notes = "What *do* data wranglers use? -- R and Python"


class R(Block):
    name = "R?" 
    shape = [[12]]
    classes = ['center']
    content = one_col_row(Img(src='/static/img/shiny.png', style={'width':'50%'}))

    
class Python(Block):
    name = "Python" 
    shape = [[9, 3]]
    row_classes = [['center-y']]
    content = [
        Markdown(
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
        Div([
            one_col_row(Img(src='/static/img/jupyter.svg', style={'width':'100%'})),
            one_col_row(Img(src='/static/img/bokeh.png')),
            one_col_row(Img(src='/static/img/dash.svg')),
        ], className='center pad-y')
    ]


    
class Dash(Block):
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [
        Markdown(
"""
* Python framework for building analytical web applications
* Enables construction of modern reactive web-apps
    - Using just Python!
* Built on
    - Flask (Python web framework)
    - React (JavaScript interface library)
"""),
        Div([
            one_col_row(Img(src='/static/img/dash.svg', style={'width':'100%'})),
            one_col_row(Img(src='/static/img/plotly.png')),
        ], className='center pad-y-extra')]

    
class DashExample(Block):
    name = "A Reactive Viz"
    shape = [
        [4, 8],
        [12]
    ]
    row_classes = [
        ['center-y'],
        []
    ]

    def get_data(self):
        self.data = {}
        csv_path = os.path.join(self.project_path, 'data', 'indicators.csv.gz')
        self.data['df'] = pd.read_csv(os.path.join(csv_path)) 
    
    @property
    def content(self):
        df = self.data['df']
        available_indicators = df['Indicator Name'].unique()
        content = {
            'content-3': Div(Markdown(
"""
    function(input1, input2, input3, input4, input5)  ==>  new_data
"""), className='center reveal', style={'font-size':'150%', 'margin-top':'2rem'}),
            'content-1':
            Div([
                one_col_row(Div([
                    Div('y-axis', style={'opacity':0.7, 'margin-bottom':'0.25rem'}),
                    Dropdown(
                        id='yaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Life expectancy at birth, total (years)'
                    ),
                    RadioItems(
                        id='yaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={})),
                one_col_row(Div([
                    Div('x-axis', style={'opacity':0.7, 'margin-bottom':'0.25rem'}),
                    Dropdown(
                        id='xaxis-column',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='Fertility rate, total (births per woman)'
                    ),
                    RadioItems(
                        id='xaxis-type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={}))
            ], className='pad-y', style={'font-size':'x-large'}),
            'content-2' :
            Div([
                Graph(id='indicator-graphic'),
                Slider(
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
        @app.callback(
            dash.dependencies.Output('indicator-graphic', 'figure'),
            [dash.dependencies.Input('xaxis-column', 'value'),
             dash.dependencies.Input('yaxis-column', 'value'),
             dash.dependencies.Input('xaxis-type', 'value'),
             dash.dependencies.Input('yaxis-type', 'value'),
             dash.dependencies.Input('year--slider', 'value')])
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
    content = one_col_row(Img(src='/static/img/dash-architecture.svg', style={'width':'70%'}))

    
class HelloWorld(Block):
    notes = "Layouts are the first main concept"
    shape = [[6, 6]]
    row_classes = [['center-y']]
    
    content = [
        Div(Markdown(
"""
    data = numpy.random.normal(size=1000) 

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
"""), className='code'),
        Div(children=[
            H2('Woah', style={'color':'red'}),
            Graph(
                id='example-graph',
                figure={
                    'data': [go.Histogram(x=numpy.random.normal(size=10000))],
                    'layout': {'title': 'Hello World'}
                }
        ),
            P('We made a thing!')

        ])
    ]

    
class Layouts(Block):
    shape = [[6, 2, 2, 2]]
    notes = "We're just building up (resuable) layout trees, like a DOM"
    content = [
        Markdown(
"""
* *Reusable* Component trees
* Components are Python classes for
    * any HTML element
    * special Dash components (eg Graph)
* Converted to JSON and sent to browser
"""),
        Div(['Div',
            Ul([
                Li('H2'),
                Li('Graph'),
                Li('P')
            ])
        ], className='clt'),
        Div(['Div',
            Ul([
                Li('H1'),
                Li(['Ul', Ul([Li('Li'), Li('Li'), Li('Li')])]),
            ])
        ], className='clt'),
        Div(['Div',
            Ul([
                Li('Markdown'),
                Li('Img'),
                Li('Img')
            ])
        ], className='clt')
    ]

    
class ReactiveHelloWorld(Block):
    shape = [[6, 6]]
    row_classes = [['center-y']]

    @property
    def content(self):
        content = [
            Div(Markdown(
"""
    app = dash.Dash()
    app.layout = html.Div([
                Graph(id='graph'),
                Slider(
                    id='slider',
                    min=10,
                    max=1000,
                    value=10,
                    step=100
                )
            ])

    @app.callback(
        Output('graph', 'figure'),
        [Input('slider', 'value')])
    def update_grapph(size):
        data = numpy.random.normal(size=size)
        return {'data': [go.Histogram(x=data)]}
"""), className='code'),
            Div([
                Graph(id='graph'),
                Slider(
                    id='slider',
                    min=10,
                    max=1000,
                    value=10,
                    step=100
                )
            ])
        ]
        return content

    def callbacks(self, app):

        @app.callback(
        dash.dependencies.Output('graph', 'figure'),
        [dash.dependencies.Input('slider', 'value')])
        def update_grapph(size):
            data = numpy.random.normal(size=size)
            return {'data': [go.Histogram(x=data)]}
    
    
class Callbacks(Block):
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [[], []]

    # callback to change the data
    # maybe also a callback to insert an image.


# TODO: slides saying callbacks are for DOM also?


class LayoutsAndCallbacks(Block):
    name = "Layouts & Callbacks"
    shape = [[4, 8]]
    row_classes = [['center-y', 'pad-top']]
    content = [Div([
            Div(['Div',
                 Ul([
                     Li('H2'),
                     Li('Graph'),
                     Li('P')
                 ])
            ], className='clt')            
        ], style={'margin-left':'3em'}),
            Div([
                Markdown(
"""
function(input1, input2, ...)  ==>  Graph.figure
""")], className='center')]


    # just show the layout tree and the original function thing
    
    
class FeatureMarkdown(Block):
    name = "Markdown" 
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [[], []]


class FeatureInterval(Block):
    name = "Interval Component" 
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [[], []]

class SinglePageApps(Block):
    shape = [[4, 8]]
    row_classes = [['center-y', 'pad-top']]
    content = [[], []]
    notes = "This plus some other magic means we can write SPAs"
    content = ['A simple URL router', Markdown(
"""
    app.callback(Output('main, 'children'), [Input('url', 'route')])
    def display_page(route):
        if route = '/':
            return home_layout
        elif route = '/viz1':
            return viz1_layout
        elif route = '/viz2':
            return viz2_layout
        else:
            return page_not_found_layout        
""")]
    
class Deployment(Block):
    name = "Deploying on the cloud"
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [
        Markdown(
"""
* Dash/Flask comes with a built-in web server
    - only meant for development
    - can only handle one request at a time
* You need a WSGI server
    - Gunicorn
    - uWSGI
    - Apache + mod_wsgi (use mod_wsgi-express)
* Will work on basically any hosting environment
"""),
        Markdown(
"""
Just Google:\\
"Hosting Flask apps on X"\\
Where X = AWS, Google Cloud, Azure, etc...
""", className='note center')
    ]
        

    
class Limitations(Block):
    shape = [[12]]
    content = Markdown(
"""
* Only supports plotly.js visualisations
    * but can create your own React components
* Involves creating a different than used for analysis
* Every reactive event requires a web request
    * slower for remotely hosted apps
    * For layout changes can create React components
    * May be forthcoming features to help
""")
    
    
class Conclusion(Block):
    name = "A Dashing Future"
    shape = [[12]]
    content = Markdown(
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



    
