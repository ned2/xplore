from itertools import chain

from exceptions import ValidationException


class Page:

    css_files = []
    js_files = []
    
    def __init__(self, app=None, title=None, url=None, index=None):
        self.app = app
        self._title = title
        self._url = url
        self.index = index

        self._validate_attrs()
        self._init_callbacks()
        
    def _validate_attrs(self):
        if not hasattr('layout'):
            msg = Page classes must define a 'layout' attribute""
            raise ValidationException(msg)
        

    def _init_callbacks(self):
        if self.app is not None and hasattr(self, 'callbacks'):
            self.callbacks(self.app)

    @property
    def css_files(self):
        if hasattr(super(), 'css_class'):
            return chain(self.__class__.css_files, super().__class__.css_files) 
        else:
            return self.__class__.css_files

    @property
    def js_files(self):
        if hasattr(super(), 'css_class'):
            return self.__class__.js_files + super().__class__.js_files 
        else:
            return self.__class__.js_files

    # TODO: give the below attributes sensible defaults for
    # when these values not provided and when not included in
    # a deck.
    
    @property
    def url(self):
        if self._url is None:
            return "page_{}".format(self.index)
        return self._url
        
    @property
    def title(self):
        if self._title is None:
            return "Page {}".format(self.index)
        return self._title
