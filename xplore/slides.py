from .page import Page
from .story import Story


class Introduction(Page):
    title = "A Story"
    layout = []
    
    def callbacks(self, app):
        pass

class MyStory(Story):
    title = "Foo"
    css_files = []
    js_files = []
    pages = [
        Introduction,
    ]
