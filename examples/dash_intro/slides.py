from dash_html_components import *
from dash_core_components import *

from xplore import Block
from xplore.layouts import *


class Title(Block):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center']
    shape = [[6, 6]]
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
But you have a finite
* time
* people
* capabilities
""", className='warning note')
    ]

    
class JavaScript(Block):
    name = "Use a JavaScript library?" 
    shape = [[8, 4]]
    content = [
        Markdown(
"""
eg D3.js, plotly.js, Chart.js, Vega etc...
* but most data analytics not done in JavaScript
* integrating data will take time
* requires front-end development skills
* full stack developers??
"""),
        Div([
            one_col_row(Img(src='/static/img/d3.png', style={'width':'30%'})),
            one_col_row(Img(src='/static/img/plotly.png')),
            one_col_row(Img(src='/static/img/chartjs.jpg')),
        ], className='center vertical-pad')
    ]

# so what do data scientists frequently code their models in?


class R(Block):
    name = "R => Shiny!" 


class Python(Block):
    name = "Python" 

    
class Dash(Block):
    pass
    
