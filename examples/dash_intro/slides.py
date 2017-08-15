from dash_html_components import *
from dash_core_components import *

from xplore.page import Page
from xplore.layouts import *


class Title(Page):
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
        ]]

    
class Context(Page):
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

    
