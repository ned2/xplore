from itertools import chain

import dash_core_components as dcc
import dash_html_components as html

from . import utils
from .exceptions import ValidationException

from .layouts import make_block_layout


class Block:

    css_files = []
    js_files = []

    
    def __init__(self, app, index, name=None, url=None):
        self.app = app
        self.index = index

        if name is not None:
            self._name = name

        if url is not None:
            self._url = url

        try:
            self.layout = self._get_layout()
            self._add_classes()
            self._add_styles()
        except ValidationException as e:
            # An error was encountered while constructing the supplied layout.
            # Construct a basic layout containing information on the error
            
            # TODO this error layout needs to be the global layout attached to
            # the Story. otherwise for multi page layouts it will just be
            # embedded somewhere in the middle of the document.
            self.layout = html.P(str(e))   

        self._init_callbacks()

    def finalise(self):
        # do things that have to happen after creation of all other blocks
        # in the story
        self._add_layout_hooks()

    def _add_layout_hooks(self):
        if 'title' in self.layout: 
            self.layout['title'].children = self.name 

        if 'next-page' in self.layout:
            link = dcc.Link(self.layout['next-page'], href=self.next_page.url)
            self.layout['next-page'] = link

        if 'prev-page' in self.layout:
            link = dcc.Link(self.layout['prev-page'], href=self.prev_page.url)
            self.layout['prev-page'] = link
            
    def _get_layout(self):
        # use of get_layout method or shape and content attrs will override a
        # layout attribute
        if hasattr(self, 'layout'):
            layout = self.layout
        elif hasattr(self, 'get_layout'):
            layout = self.get_layout()  
        elif hasattr(self, 'shape') and hasattr(self, 'content'): 
            # possibly could make content optional; not sure what someone would
            # do with the content-less layout tree
            layout = make_block_layout(shape=self.shape, content=self.content)
        else:
            msg = "Block subclasses must either define a 'layout' attribute, " \
                  "a 'get_layout' method, or both 'shape' and 'content' attributes."
            raise ValidationException(msg)
        return layout
    
    def _add_classes(self):
        if hasattr(self, 'classes'):
            new_classes = self.classes

            curr_classes = getattr(self.layout, 'className', None)
            if curr_classes is not None:
                new_classes = self.classes + [curr_classes]
                
            self.layout.className = " ".join(new_classes)

    def _add_styles(self):
        if hasattr(self, 'style'):
            self.layout.style = self.style
        
    def _init_callbacks(self):
        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)

    @property
    def all_css_files(self):
        if hasattr(super(), 'css_class'):
            return chain(super().__class__.css_files, self.__class__.css_files) 
        else:
            return self.__class__.css_files

    @property
    def all_js_files(self):
        if hasattr(super(), 'js_class'):
            return chain(super().__class__.js_files, self.__class__.js_files) 
        else:
            return self.__class__.js_files
        
    @property
    def url(self):
        if not hasattr(self, '_url'):
            self._url = utils.slugify(self.name)
        return self._url
        
    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = utils.camel_case_to_title(self.__class__.__name__)
        return self._name
