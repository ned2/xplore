from itertools import chain

from .exceptions import ValidationException


def slugify(text):
    return text.strip().lower().replace(' ', '-')


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
            self._url = slugify(self.name)
        return self._url
        
    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = self.__class__.__name__
        return self._name
