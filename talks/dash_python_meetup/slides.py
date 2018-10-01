import os
from textwrap import dedent

import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from xplore import Block
from xplore.layouts import *
from xplore.components import Col, Row, Image, FontA, Box, BackgroundImage

def s(string):
    return dedent(string).strip()


# Time: 30 minutes

class Title(Block):
    name = "Building Data-driven Web Applications with Dash"
    title = True
    shape = [[6, 6]]
    row_classes = ['pad-top']
    content = [
        html.Div(dcc.Markdown(dedent("""
        ### Ned Letcher
        nedned.net  
        @nletcher"""))),
        html.Div([
            Image(src='dash.svg'),
            Image(src='plotly.png')
        ], className='d-flex flex-column')
    ]

class UserInterfaces(Block):
    name = "Sometimes you need a User Interface"
    header = True
    shape = [[8,4]]
    content = [
        dcc.Markdown(s(
            """
            * Business intelligence, analytics
              - dashboards, KPIs etc
              - interactive reports
            * Research, science, data science
              - interactive exploration of results
              - vehicle for communicating results 
              - prototypes
            * DevOps, site reliability engineers (SREs)
              - monitoring dashboards
            * Data-driven journalism
              - interactive content
              - explorable explanations
            * Web Development
              - rapid prototyping 
            """
        )),
        Image('charts.svg', round=True),        
    ]



class Context(Block):
    name = "Sometimes you need a User Interface"
    header = True
    shape = [[6, 6], [12], [6, 6]]

    content = [
        Image('table.png', round=True, width=65),
        Image('code.jpg', round=True, width=50),
        FontA('fa-arrow-down fa-5x'),
        Image('charts.svg', round=True, width=50),
        Image('interfaces.jpg', round=True, width=50),
    ]


class Requirements(Block):
    header = True
    shape = [[None]]
    content = [
        dcc.Markdown(s(
            """
            * **Reactive**
              - Responsive interface that users can interact with  
            * **Sharable/accessible**
              - Readily accessible by the target audience
            * **Deployable**
              - Offer a familiar pathway for deployment
            * **Scalable**
              - Should offer a pathway to servicing large-scale 
            ---
            **Some options**
            * Jupyter Notebook/ Jupyter Lab
            * R Shiny
            """)
        ),
    ]


class WebPlatform(Block):
    name = "The Web Platform?"
    header = True
    content = Image('web.png', width=80)


# TODO: add floating text indicating point of the slide
# (does background image want to be a Block class attribute?)
class Madness(Block):
    content = BackgroundImage(src='js_madness.png')

    
# TODO: add floating text indicating point of the slide
class Glue(Block):
    content = BackgroundImage(src='switchboard.jpg')


class WeWant(Block):
    header = True
    shape = [[6]]
    content = Box(dcc.Markdown(s(
        """
        A simple framework for rapidly developing interactive web applications
        *within* Python.
        """)
    ), center=True)


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
        dcc.Markdown(s(
            """
            * Framework for building data-driven reactive web applications
            - __*using only Python!!*__
            * Made by Plotly
            * Open source (MIT Licence)
            * Active community
            * ~6k ★ on GitHub
            """)
        )
    ]

    
class Meta(Block):
    content = Image(src='whatifitoldyou.jpg')


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

    
class Layout(Block):
    title = True

    
class Components(Block):
    header = True    
    shape = [[12], [12], [4,4,4]]
    content = [
        html.P("""
            Dash Components are React components that
            are serialised into Python classes."""),
        html.Div(
            className="tree",
            children=html.Ul([
                html.Li([
                    html.A("Component"),
                    html.Ul([
                        html.Li(html.A("Dash HTML Component",
                                       className="html-component")),
                        html.Li(html.A("Dash Core Component",
                                       className="dcc-component")),
                        html.Li(html.A("Custom Dash Component",
                                       className="custom-component")),
                    ])
                ])
            ])
        ),
        html.Ul([
            html.Li("Div"),
            html.Li("Img"),
            html.Li("H1, H2, H3"),
            html.Li("P"),
            html.Li("et cetera..."),
        ]),
        html.Ul([
            html.Li("Graph"),
            html.Li("Dropdown"),
            html.Li("Slider"),
            html.Li("Textarea"),
            html.Li("DatePickerRange"),
            html.Li("Markdown"),
            html.Li("and more..."),
        ]),
        html.Div()
    ]
    

class ComponentTrees(Block):
    name = "Layouts are Component Trees"
    header = True
    # not using shape because I haven't worked out a way to selctively make
    # bootstrap cols produced by shape *not* horizontally centered
    content = html.Div([
        Row([
            html.Div(),
            dcc.SyntaxHighlighter(
                language='python',
                theme='dark',           
                children=s("""
                import dash_html_components as html
                import dash_core_components as dcc
                """)
            )
        ], style={'width':'50vw'}),
        Row([
            html.Div([
                html.A('Div', className="html-component"),
                html.Ul([
                    html.Li(html.A('H1', className="html-component")),
                    html.Li(html.A('Graph', className="dcc-component")),
                    html.Li(html.A('P', className="html-component")),
                ])
            ], className='clt'),
            dcc.SyntaxHighlighter(
                language='python',
                theme='dark',    
                children=s(
                    """
                    html.Div([
                        html.H1("My Dashboard"),
                        dcc.Graph(),
                        html.P("We did a dashboard")
                    ])
                    """))
        ], className='m-2'),
        Row([
            html.Div([
                html.A('Div', className="html-component"),
                html.Ul([
                    html.Li(html.A('H1', className="html-component")),
                    html.Li([
                        html.Div(html.A('Ul', className="html-component")),
                        html.Ul([
                            html.Li(html.A('Li', className="html-component")),
                            html.Li(html.A('Li', className="html-component")),
                            html.Li(html.A('Li', className="html-component")),
                        ])
                    ]),
                ])
            ], className='clt'),
            dcc.SyntaxHighlighter(
                language='python',
                theme='dark',           
                children=s(
                    """
                    html.Div([
                        html.H1('My List'),
                        html.Ul([
                            html.Li(),
                            html.Li(),
                            html.Li(),
                        ]),
                    ])
                    """)
            )
        ], className='m-2'),
        Row([
            html.Div([
                html.A('Div', className="html-component"),
                html.Ul([
                    html.Li(html.A('Markdown', className="dcc-component")),
                    html.Li(html.A('Img', className="html-component")),
                    html.Li(html.A('Img', className="html-component")),
                ])
            ], className='clt'),
            dcc.SyntaxHighlighter(
                language='python',
                theme='dark',           
                children=s("""
                html.Div([
                    dcc.Markdown('''
                        # Some Markdown Content
                        _Everybody_ loves Markdown'''),
                    html.Img(src="image1.png"),
                    html.Img(src="image2.png"),
                ])
                """)
            )
        ])
    ])
    
    
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
                children=s(
                    """
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
                    """)
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


# TODO 

# Add:
# -- can only target one output element
# -- each element-property pair can only be the output of one callback
# -- can target layout     
class Callbacks(Block):
    header = True
    hcenter = False
    vcenter = False
    shape = [[12], [7, 5], [7, 5]]
    content = [
        dcc.Markdown("Callbacks are Python decorators that make your app reactive."),
        dcc.SyntaxHighlighter(
            language="python",
            theme="dark",
            children=s(
                """
                @app.callback(
                    Output('output-box', 'children'),
                    [State('input', 'value')],
                    [Input('slider', 'value'), Input('dropdown', 'value')])
                def update(state1, input1, input2):
                    return html.Div([
                        html.Div(f"Input 1: {input1}"),
                        html.Div(f"Input 2: {input2}"),
                        html.Div(f"State 1: {state1}"),
                    ])
                """)
        ),
        dcc.Markdown(s(
            """
            They have:
            * one **Output**
            * zero or more **States**
            * one or more **Inputs**
            """)
        ),
        dcc.SyntaxHighlighter(
            language="python",
            theme="dark",
            children=s(
                """
                html.Div([
                    html.Div('Input 1:'),
                    dcc.Slider(id='slider', min=0, max=10, step=1, value=1),
                    html.Div('Input 2:'),
                    dcc.Dropdown(
                        id='dropdown', value='eggs',
                        options=[
                            {'label': 'Spam', 'value': 'spam'},
                            {'label': 'Eggs', 'value': 'eggs'}
                        ],
                    ),
                    html.Div('State 1:'),
                    dcc.Input(id='input', value='state', type='text'),
                    html.Div(id='output-box')
                ])
                """)
        ),
        html.Div([
            html.Div('Input 1:'),
            dcc.Slider(
                id='slider',
                min=0,
                max=10,
                step=1,
                value=1
            ),
            html.Div('Input 2:'),
            dcc.Dropdown(
                id='dropdown',
                value='eggs',
                options=[
                    {'label': 'Spam', 'value': 'spam'},
                    {'label': 'Eggs', 'value': 'eggs'}
                ],
            ),
            html.Div('State 1:'),
            dcc.Input(
                id='input',
                value='state',
                placeholder='state',
                type='text'
            ),
            html.Div(id='output-box', className='output-box')
        ]),
    ]

    def callbacks(self, app):
        @app.callback(
            Output('output-box', 'children'),
            [Input('slider', 'value'), Input('dropdown', 'value')],
            [State('input', 'value')]
        )
        def update(input1, input2, state1):
            return html.Div([
                html.Div(f"Input 1: {input1}"),
                html.Div(f"Input 2: {input2}"),
                html.Div(f"State 1: {state1}"),
            ])


    
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
                children=s(
                    """
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
                    """)
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


class MarkdownComponent(Block):
    header = True
    shape = [[6, 6]]
    content = [
        dcc.SyntaxHighlighter(
            language='python',
            theme='dark',
            children=
'''
app.layout = dcc.Markdown("""
Markdown
--------
An easy to read and write **markup** language
* automatically converted to HTML
* _greatly_ simplifies content creation
 """)
'''.strip())
        ,
        dcc.Markdown(
"""
Markdown
--------
An easy to read and write **markup** language
* automatically converted to HTML
* _greatly_ simplifies content creation
""")]


class DashComponents(Block):
    title = True
    name = "What's in the Box?"


# TODO
class MiscComponents(Block):
    title = True

    
# TODO    
class DataTableComponentImage(Block):
    content = Image(src='datatable.png', width=80)


#TODO
class TabsComponent(Block):
    title = True


class DataTableComponent(Block):
    header = True

    def get_data(self):
        df = pd.read_csv(
            'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
        )
        df = df[df['year'] == 2007]
        df[0:20]
        self.data = df

    @property    
    def content(self):
        return html.Div([
            html.H4('Gapminder DataTable'),
            # dt.DataTable(
            #     rows=self.data.to_dict('records'),
            #     # optional - sets the order of columns
            #     columns=sorted(self.data.columns),
            #     row_selectable=True,
            #     filterable=True,
            #     sortable=True,
            #     selected_row_indices=[],
            #     id='datatable-gapminder'
            # ),
            html.Div(id='selected-indexes'),
            dcc.Graph(id='graph-gapminder'),
        ], className="container")

    def callbacks(self, app):
        @self.app.callback(
            Output('datatable-gapminder', 'selected_row_indices'),
            [Input('graph-gapminder', 'clickData')],
            [State('datatable-gapminder', 'selected_row_indices')])
        def update_selected_row_indices(clickData, selected_row_indices):
            if clickData:
                for point in clickData['points']:
                    if point['pointNumber'] in selected_row_indices:
                        selected_row_indices.remove(point['pointNumber'])
                    else:
                        selected_row_indices.append(point['pointNumber'])
            return selected_row_indices

        @self.app.callback(
            Output('graph-gapminder', 'figure'),
            [Input('datatable-gapminder', 'rows'),
             Input('datatable-gapminder', 'selected_row_indices')])
        def update_figure(rows, selected_row_indices):
            dff = pd.DataFrame(rows)
            fig = plotly.tools.make_subplots(
                rows=3, cols=1,
                subplot_titles=('Life Expectancy', 'GDP Per Capita', 'Population',),
                shared_xaxes=True)
            marker = {'color': ['#0074D9']*len(dff)}
            for i in (selected_row_indices or []):
                marker['color'][i] = '#FF851B'
            fig.append_trace({
                'x': dff['country'],
                'y': dff['lifeExp'],
                'type': 'bar',
                'marker': marker
            }, 1, 1)
            fig.append_trace({
                'x': dff['country'],
                'y': dff['gdpPercap'],
                'type': 'bar',
                'marker': marker
            }, 2, 1)
            fig.append_trace({
                'x': dff['country'],
                'y': dff['pop'],
                'type': 'bar',
                'marker': marker
            }, 3, 1)
            fig['layout']['showlegend'] = False
            fig['layout']['height'] = 800
            fig['layout']['margin'] = {
                'l': 40,
                'r': 10,
                't': 60,
                'b': 200
            }
            fig['layout']['yaxis3']['type'] = 'log'
            return fig

        
class Extensible(Block):
    name = "Extensible Components"
    header = True
    shape = [[12]]
    content = dcc.Markdown(
"""
* Dash layout components are React components
   - Can create custom own Dash layout components
   - existing React components can be converted to Dash components
   - Plotly has a toolchain for streamlining creation components  
   - Can be added to the open source Dash library for all to benefit
""")


    
# TODO:
# -- think of better name
# -- rework the slide contents
class CallbackData(Block):
    header = True
    shape = [[6, 6]]
    content =[
        Box("Callbacks are stateless"),
        dcc.Markdown("""
* All callbacks share the same memory
* Treat underlying data as immutable
* No globals!

This means:
* callbacks can run concurrently
  - through either multiple threads or worker processes 
* can cache output of callbacks
""")]


class SinglePageApps(Block):
    shape = [[3, 9]]
    header = True
    content = [
        'A simple URL router',
        dcc.SyntaxHighlighter(
            language="python",
            theme="dark",
            children="""
app.callback(Output('main', 'children'), [Input('url', 'route')])
def display_page(route):
    if route = '/':
        return home_layout
    elif route = '/page-a':
        return page_a_layout
     elif route = '/page-b':
        return page_b_layout
    else:
        return page_not_found_layout
""".strip())
    ]


class Deployment(Block):
    name = "Deploying on the cloud"
    shape = [[8, 4]]
    row_classes = ['center-y']
    content = [
        dcc.Markdown(s(
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
            """)),
        dcc.Markdown(s(
            """
            Just Google:\\
            "Hosting Flask apps on X"\\
            Where X = AWS, Google Cloud, Azure, etc...
            """), className='note center')
    ]



class Limitations(Block):
    header = True
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


class Conclusion(Block):
    header = True
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
