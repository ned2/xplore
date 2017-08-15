from dash_html_components import *
from dash_core_components import *

from xplore.page import Page
from xplore.layouts import *


class Title(Page):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center', 'row-buffers']
    
    def get_layout(self):
        content = [
            Markdown(
"""
### Ned Letcher
@nletcher
"""),
            Img(src='/static/img/forefront.jpg'),
            Img(src='/static/img/melbourne-uni.png', style={'width':'15%'}),
        ]
        layout = page([1,1,1], content=content)
        return layout


    
class IsThisWorking(Page):
    layout = Div([
        H1(id='title'),
        P('Next', id='next-page')
    ])

    def callbacks(self, app):
        pass

    
