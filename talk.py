import dash_html_components as html
import dash_core_components as dcc

from xplore.page import Page
from xplore.story import Story

from flask import Flask, send_from_directory

class Introduction(Page):
    layout = html.Div([
        html.H1('Introduction'),
        dcc.Link('hey', href='hey')
    ])

    
class Hey(Page):
    layout = html.Div([
        html.H1('Hey'),
        dcc.Link('intro', href='introduction')
    ])

    def callbacks(self, app):
        pass

    
class DashTalk(Story):
    title = "Creating Reactive Web Apps in Python"
    css_files = ['hi']
    js_files = []
    pages = [
        Introduction,
        Hey,
    ]

# TODO
# -- create javascript file to include that binds back and forwards
#    keys to previous next link (also 'h' for home?) 
# -- create default light and dark themes


# next: get this thing running!!

talk = DashTalk()

# register the static route with Flask
# @talk.app.server.route('/static/xplore.css')
# def send_static():
#     print('foo')
#     return send_from_directory('static', 'xplore.css')

if __name__ == '__main__':
    talk.app.server.run(debug=True)
