import dash_html_components as html
import dash_core_components as dcc

from xplore.page import Page
from xplore.story import Story


class Introduction(Page):
    layout = html.H1('Introduction')
    
    def callbacks(self, app):
        pass

class DashTalk(Story):
    title = "Creating Reactive Web Apps in Python"
    css_files = []
    js_files = []
    pages = [
        Introduction,
    ]

# TODO
# -- create javascript file to include that binds back and forwards
#    keys to previous next link (also 'h' for home?) 
# -- create default light and dark themes


# next: get this thing running!!

talk = DashTalk()

if __name__ == '__main__':
    talk.app.server.run(debug=True)
