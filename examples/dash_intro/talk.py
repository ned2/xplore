from dash_html_components import *
from dash_core_components import *

from xplore.page import Page
from xplore.story import Story
from xplore.layouts import *


# TODO:
# start writing the talk
# I'm at a point where all styling can be done after the fact.
# start with intro slide and get on it :)

class Title(Page):
    name = "Creating Reactive Web Apps in Python"

    # TODO
    # classes = []
    # styles = []
    
    def get_layout(self):
        layout = page()
        layout['content-1'] = Markdown(
"""
### hello!

Scenario
* hello blah
* foo
"""
        )
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
    css_files = []
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
