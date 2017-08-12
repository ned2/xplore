import os

from dash.dependencies import Input, Output
from dash import Dash

from .story import Story
from . import layouts
from . import slides











    
# try and keep the layout and slide/story classes separated until such time as it
# becomes obvious they want to be combined

story = MyStory(app, index_type='outline')
app.layout = layouts.main()
app.layout['navbar'] = layouts.navbar(story.nav_items)

        
@app.callback(Output('page', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    default_layout = layouts.url_not_found(pathname)
    layout = story.urls.get(pathname, default_layout)
    return layout


if __name__ == '__main__':
    app.run_server(debug=True)
