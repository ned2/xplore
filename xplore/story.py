import sys
import importlib
import inspect
from itertools import chain
from collections import Mapping

from dash import Dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component
from flask import Flask, send_from_directory

from . import layouts
from .exceptions import ValidationException


class AttrDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    
def load_settings(module):
    settings = AttrDict()
    for setting in dir(module):
        if setting.isupper():
            settings[setting.lower()] = getattr(module, setting)
    return settings


class Story:

    css_files = []
    js_files = []

    # available settings that can be configured
    settings_attrs = (
        'page_element_id',
        'navbar_element_id',
        'static_file_path',
        'index_page_layout',
        'index_page_type',
        'route_not_found_layout',
        'navbar',
    )

    index_page_options = (
        'outline',
        'first',
        'vertical'
    )

    # TODO -- add navbar orientation flag, horizontal/vertical
    def __init__(self, app=None, server=None, settings=None, **settings_kwargs):
        # load the settings
        if settings is None:
            settings_module = importlib.import_module('.settings', __package__)
            self.settings = load_settings(settings_module)
        elif isinstance(settings, str):
            app_path = inspect.getfile(self.__class__)
            sys.path.append(app_path)
            settings_module = importlib.import_module(settings)
            self.settings = load_settings(settings_module)
        elif isinstance(Mapping):
            self.settings = settings
        else:
            msg = "'settings' parameter must a string containing the name of " \
                  "a settings module or a dict-like object containing " \
                  "setting names and values."
            raise ValidationException(msg)

        for setting in self.settings_attrs:
            # update current settings with those specified as parameters
            value = settings_kwargs.get(setting, None)
            if value is not None:
                self.settings[setting] = value            
            
        # users can supply their own Dash app instance, or one will be created
        if app is not None:
            self.app = app
        else:
            if server is not None:
                self.app = Dash(server=server)
            else:
                self.app = Dash()

        self._init_app()
        self._set_index_route()
        self._validate_attrs()

    def _init_app(self):
        self.app.title = self.title
        self.app.layout = layouts.main()

        if self.settings.navbar:
            nav_layout = layouts.navbar(self.nav_items)
            self.app.layout[self.settings.navbar_element_id] = nav_layout
            
        # Dash complains about callbacks on nonexistent elements otherwise
        #self.app.config.supress_callback_exceptions = True

        # register the router callback with Dash
        @self.app.callback(Output(self.settings.page_element_id, 'children'),
              [Input('url', 'pathname')])
        def display_page(pathname):
            # users can supply a default layout which can either be
            # a dash component. a callable that returns a dash layout
            if self.settings.route_not_found_layout is None:
                default_layout = layouts.url_not_found(pathname)
            elif isinstance(self.settings.route_not_found_layout, Component):
                default_layout = self.settings.route_not_found_layout
            elif callable(self.settings.route_not_found_layout):
                default_layout = self.settings.route_not_found_layout(pathname)
            else:
                # TODO raise validation error
                pass
            return self.routes.get(pathname, default_layout)
        
        # register the static route with Flask
        @self.app.server.route('/{}/<path:path>'.format(
            self.settings.static_file_path))
        def send_static(path):
            return send_from_directory('static', path)

        # register all CSS files with app
        for css_path in self.css_files:
            full_css_path = self._get_static_path(css_path) 
            self.app.css.append_css({"external_url": full_css_path})

        # register all JS files with app
        for js_path in self.js_files:
            full_js_path = self._get_static_path(js_path) 
            self.app.css.append_css({"external_url": full_js_path})

    def _set_index_route(self):
        # if index_layout is specified, then we use this for the index page
        # of the story. otherwise, a layout is created according to the value 
        # of settings.index_page_type
        if self.settings.index_page_layout is None:
            if self.settings.index_page_type == 'first':
                self.settings.index_page_layout = self.page_list[0].layout
            elif self.settings.index_page_type == 'outline':
                # TODO
                pass
            elif self.settings.index_page_type == 'vertical':
                # TODO
                pass
            else:
                msg = "'index_page_type' param must be one of {}"
                raise ValidationException(msg.format(format(index_page_options)))
        self.register_route('/', self.settings.index_page_layout)
            
    def _validate_attrs(self):
        if not hasattr(self, 'app'):
            msg = "Page classes must define an 'app' attribute"
            raise ValidationException(msg)

    def _get_static_path(self, path):
        return '/'.join(self.settings.static_file_path.rstrip('/'), path)

    def register_route(self, route, layout):
        self.routes[route] = layout
        
    @property
    def page_list(self):
        """create the pages from the list of Page classes in 'pages' attr"""
        if not hasattr(self, '_page_list'):
            self._page_list = []
            for i, cls in enumerate(self.pages):
                page = cls(self.app, i + 1) 
                self._page_list.append(page)
        return self._page_list

    @property
    def routes(self):
        if not hasattr(self, '_routes'):
            self._routes = {}
            for page in self.page_list:
                self.register_route('/'+page.url, page.layout)
                self.register_route('/'+str(page.index), page.layout)
        return self._routes

    @property
    def css_files(self):
        # returns a generator yielding all CSS files attached to pages used in
        # this story as well as those attached to this story
        pages_css = (page.css_files for page in self.page_list)
        return chain(self.__class__.css_files, *pages_css)
    
    @property
    def js_files(self):
        # returns a generator yielding all JS files attached to pages used in this
        # story as well as those attached to this story
        pages_css = (page.js_files for page in self.page_list)
        return chain(self.__class__.js_files, *pages_css)
    
    @property
    def nav_items(self):
        return [(page.url, page.title) for page in self.page_list]
