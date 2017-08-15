from dash_html_components import *
from dash_core_components import *

from xplore.page import Page
from xplore.story import Story
from xplore.layouts import *


# Possible dash bug:
# -- img with no 'src' attribute specified seems to be triggering the
#    URL callback with a pathname of None
# -- also Img with a 'style' attr that is a string instead of a dict



# Various issues:
# 
# I am automatically prefixing static dir for CSS and JS urls but not for
# images.



class Title(Page):
    name = "Creating Reactive Web Apps in Python"
    classes = ['center', 'row-buffers']
    
    def get_layout(self):
        content = [
            P('Ned Letcher'),
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

    
class DashTalk(Story):
    title = "Creating Reactive Web Apps in Python"
    css_files = ['css/talk.css']
    js_files = []

    pages = [
        Title, 
        IsThisWorking,
    ]

# TODO
# -- create javascript file to include that binds back and forwards
#    keys to previous next link (also 'h' for home?) 
# -- create default light and dark themes



talk = DashTalk()

if __name__ == '__main__':
    talk.app.server.run(debug=True)
