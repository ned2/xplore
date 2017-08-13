from itertools import chain

import dash_core_components as dcc

from . import utils
from .exceptions import ValidationException


class Page:

    css_files = []
    js_files = []
    
    def __init__(self, app, index, name=None, url=None):
        self.app = app
        self.index = index

        if name is not None:
            self._name = name

        if url is not None:
            self._url = url

        self._validate_attrs()
        self._init_callbacks()

    def finalise(self):
        # do things that have to happen after creation of all other pages
        # in the story
        self._add_layout_hooks()

    def _add_layout_hooks(self):
        if 'title' in self.layout: 
            self.layout['title'].children = self.name 
        if 'next-page' in self.layout:
            link = dcc.Link(self.layout['next-page'], href=self.next_page.url)
            self.layout['next-page'] = link
            
    def _validate_attrs(self):
        if not hasattr(self, 'layout'):
            msg = "Page classes must define a 'layout' attribute"
            raise ValidationException(msg)        

    def _init_callbacks(self):
        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)

    @property
    def all_css_files(self):
        if hasattr(super(), 'css_class'):
            return chain(self.__class__.css_files, super().__class__.css_files) 
        else:
            return self.__class__.css_files

    @property
    def all_js_files(self):
        if hasattr(super(), 'css_class'):
            return self.__class__.js_files + super().__class__.js_files 
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
