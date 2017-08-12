from itertools import chain

from dash import Dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component

from flask import Flask, send_from_directory, redirect

import settings
from . import layouts


class Story:

    css_files = []
    js_files = []

    # index options:
    #   'outline'  
    #   'first'
    #   'page'
    def __init__(self, app=None, layout=None, navbar=True,
                 index_page_type=settings.INDEX_PAGE_TYPE,
                 static_file_path=settings.STATIC_FILE_PATH,
                 route_not_found_layout=None):

        # users can supply their own Dash app instance, or one will be created
        # along with a Flask instance
        if app is not None:
            self.app = app
        else:
            self.app = Dash(__name__, server=Flask(__name__))
            
        self.static_file_path = static_file_path 
        self.index_page_type = index_page_type
        self.route_not_found_layout = route_not_found_layout
        self.navbar = navbar

        # initialize various Dash app 
        self._init_app()
        self._validate_attrs()

        # if index_layout is specified, then we use this for the index page
        # of the story. otherwise, a layout is created according to the value 
        if index_layout is not None:
            self.index_layout = index_layout
        else:
            self.index_layout = make_index_layout(index_page_type)

        self.register_route('/', self.index_layout)

    def _init_app(self):
        self.app.title = self.title
        self.app.layout = layouts.main()

        if self.navbar:
            self.app.layout[settings.NAVBAR_ID] = layouts.navbar(self.nav_items)
            
        # Dash complains about callbacks on nonexistent elements otherwise
        self.app.config.supress_callback_exceptions = True

        # register the router callback
        @self.app.callback(Output(settings.PAGE_ELEMENT_ID, 'children'),
              [Input('url', 'pathname')])
        def display_page(pathname):
            # users can supply a default layout which can either be
            # a dash component. a callable that returns a dash layout
            if self.route_not_found_layout is None:
                default_layout = layouts.url_not_found(pathname)
            elif isinstance(self.route_not_found_layout, Component):
                default_layout = self.route_not_found_layout
            elif callable(self.route_not_found_layout):
                default_layout = self.route_not_found_layout(pathname)
            return self.urls.get(pathname, default_layout)
        
        # register the static route
        @self.server.route('/{}/<path:path>'.format(self.static_file_path))
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

    def _validate_attrs(self):
        if not hasattr('app'):
            msg = "Page classes must define an 'app' attribute"
            raise ValidationException(msg)

    def _get_static_path(self, path):
        return '/'.join(self.static_file_path.rstrip('/'), path)

    def register_route(route, layout):
        self._routes[route] = layout
        
    @propety
    def page_list(self):
        """create the pages from the list of Page classes in 'pages' attr"""
        if not hasattr(self, '_page_list'):
            self._page_list = []
            for i, cls in enumerate(self.pages):
                page = cls(
                    app=self.app,
                    index=i
                ) 
                self._page_list.append(page)
        return self._page_list

    @property
    def routes(self):
        if not hasattr(self, '_routes'):
            self._routes = {}
            for page in self.page_list:
                self.register_route(page.url, page.layout):
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
