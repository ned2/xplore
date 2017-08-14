import dash_html_components as html
import dash_core_components as dcc

from xplore.page import Page
from xplore.story import Story


class Introduction(Page):
    name = "Creating Reactive Web Apps in Python"
    layout = html.Div([
        html.H1(id='title'),
        dcc.Markdown("""
### hello!

Scenario
* hello blah
* foo
        """),
        html.P('Next', id='next-page')
    ])

    
class IsThisWorking(Page):
    layout = html.Div([
        html.H1(id='title'),
        html.P('Next', id='next-page')
    ])

    def callbacks(self, app):
        pass

    
class DashTalk(Story):
    title = "Creating Reactive Web Apps in Python"
    css_files = []
    js_files = []

    pages = [
        Introduction,
        IsThisWorking,
    ]

# TODO
# -- create javascript file to include that binds back and forwards
#    keys to previous next link (also 'h' for home?) 
# -- create default light and dark themes



talk = DashTalk()

if __name__ == '__main__':
    talk.app.server.run(debug=True)
