import sys
import os
import importlib
import inspect
from itertools import chain
from collections import Mapping, defaultdict

from dash import Dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component
from flask import Flask, send_from_directory

from . import layouts
from .exceptions import ValidationException


class AttrDict(defaultdict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    
def load_settings(module):
    settings = AttrDict(lambda :None)
    for setting in dir(module):
        if setting.isupper():
            settings[setting.lower()] = getattr(module, setting)
    return settings


class Story:

    css_files = [
        'xplore/css/xplore.css',
        'xplore/font/source-sans-pro/source-sans-pro.css',
    ]
    js_files = []

    # available settings that can be configured
    settings_attrs = (
        'page_element_id',
        'navbar_element_id',
        'static_url_path',
        'static_folder',
        'index_page_layout',
        'index_page_type',
        'route_not_found_layout',
        'root_path',
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

        self._init_app(server)
        self._set_index_route()
        self._validate_attrs()

    def _init_app(self, server):
        if server is None:
            flask_kwargs = {}
            for param in ('static_url_path', 'static_folder'):
                if self.settings[param] is not None:
                    flask_params[param] = self.settings[param]
            server = Flask(__name__, **flask_kwargs)

        self.app = Dash(name=__name__, server=server)
        self.app.title = self.title
        self.app.layout = layouts.main()

        if self.settings.navbar:
            nav_layout = layouts.navbar(self.nav_items)
            self.app.layout[self.settings.navbar_element_id] = nav_layout
            
        # Dash complains about callbacks on nonexistent elements otherwise
        self.app.config.supress_callback_exceptions = True

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
        @self.app.server.route('{}/xplore/<path:path>'.format(
            self.app.server.static_url_path))
        def send_static(path):
            static_path = os.path.join(self.xplore_base_path, 'static')
            return send_from_directory(static_path, path)

        # register all CSS files with app
        for css_path in self.all_css_files:
            full_css_path = self._get_static_path(css_path) 
            self.app.css.append_css({"external_url": full_css_path})

        # register all JS files with app
        for js_path in self.all_js_files:
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
        pass
        # if not hasattr(self, 'app'):
        #     msg = "Page classes must define an 'app' attribute"
        #     raise ValidationException(msg)

    def _get_static_path(self, path):
        return '{}/{}'.format(self.app.server.static_url_path.rstrip('/'), path)

    def register_route(self, route, layout):
        self.routes[route] = layout

    @property
    def xplore_base_path(self):
        return os.path.dirname(os.path.realpath(__file__))
    
    @property
    def page_list(self):
        """create the pages from the list of Page classes in 'pages' attr"""
        if not hasattr(self, '_page_list'):
            self._page_list = []
            prev_page = None
            for i, cls in enumerate(self.pages):
                # create the page
                page = cls(self.app, i + 1)

                # link the previous page's 'next_page' attr to this one
                if prev_page is not None:
                    prev_page.next_page = page
                self._page_list.append(page)
                prev_page = page

            # link the last page to the first page    
            prev_page.next_page = self._page_list[0]

            # finalise each page with stuff that has to happen after
            # the creation of all the pages
            for page in self._page_list:
                page.finalise()
                
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
    def all_css_files(self):
        # returns a generator yielding all CSS files attached to pages used in
        # this story as well as those attached to this story
        pages_css = (page.all_css_files for page in self.page_list)
        return chain(Story.css_files, *pages_css)
    
    @property
    def all_js_files(self):
        # returns a generator yielding all JS files attached to pages used in this
        # story as well as those attached to this story
        pages_js = (page.all_js_files for page in self.page_list)
        return chain(Story.js_files, *pages_js)
    
    @property
    def nav_items(self):
        return [(page.url, page.title) for page in self.page_list]
