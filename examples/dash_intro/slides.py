from dash_html_components import *
from dash_core_components import *

from xplore.page import Page
from xplore.layouts import *


class Title(Page):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center', 'row-buffers']
    shape = [[12],[12],[12]]
    content = [
        Markdown(
"""
#### Ned Letcher
@nletcher\\
nedned.net
"""),
            Img(src='/static/img/forefront.jpg'),
            Img(src='/static/img/melbourne-uni.png', style={'width':'15%'}),
        ]

    
class Context(Page):
    name = "So you have some data" 
    shape = [[6, 4]]
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
But you have a finite amount of
* time
* people
* skills
""", className='warning note')
    ]

    
