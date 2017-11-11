import sys
import os
import random
import string
import importlib
import inspect
from itertools import chain
from collections import Mapping

import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component
from flask import Flask, send_from_directory

from . import layouts, utils, config
from .exceptions import ValidationException

# Grand plan:
#
# content params should be able to take pages as values.

# This will mean that the ID for each block will need to have an index
# change page ID setting to something like BLOCK_ID_PREFIX = 'block

# as it stands I think maybe I've somewhat coupled the make_block_layout
# function to the presentation module thing. how to reconcile?



class Xplorable:

    def __init__(
            self,
            server=None,
            static_folder='static',
            index_page_type='first',
            route_not_found_layout=None):

        self.static_folder = static_folder
        self.route_not_found_layout = route_not_found_layout
        self.index_page_type = index_page_type

        if server is None:
            server = self._make_flask_server()

        self.app = Dash(name=__name__, server=server)
        self.app.config.suppress_callback_exceptions = True
        self._init_pages()
        self._init_app()
        self._register_routes()

        # finalise each page with stuff that has to happen after the creation of
        # all the pages
        for page in self.page_list:
            page.finalise()

    def _make_flask_server(self):
        # create a Flask instance, giving it the static folder to use 
        return Flask(
            __name__,
            static_folder=os.path.join(self.project_path, self.static_folder)
        )
            
    def _init_pages(self):
        self.page_list = []
        prev_page = None
        for i, cls in enumerate(self.pages):
            # create the page
            page = cls(self.app, i + 1, self.project_path)

            if prev_page is not None:
                # link this page to the last one
                page.prev_page = prev_page
                prev_page.next_page = page

            self.page_list.append(page)
            prev_page = page

        # link the last page to the first page    
        prev_page.next_page = self.page_list[0]

        # link the first page to the last page
        self.page_list[0].prev_page = prev_page
        
    def _init_app(self):
        self.app.title = self.title

        # add the layout
        self.app.layout = self._get_layout()
        
        # register the router callback with Dash
        @self.app.callback(Output(config.PAGE_ELEMENT_ID, 'children'),
              [Input('url', 'pathname')])
        def display_page(pathname):
            if self.route_not_found_layout is None:
                default_layout = html.P("No page '{}'".format(pathname))
            else:
                default_layout = self.route_not_found_layout(pathname)

            # look up the path name from the routes
            return self.routes.get(pathname, default_layout)
        print(self.app.server.static_url_path)
        # register xplore's static route with Flask
        @self.app.server.route('{}/xplore/<path:path>'.format(
            self.app.server.static_url_path))
        def send_static(path):
            static_path = os.path.join(self.xplore_base_path,
                                       config.STATIC_PATH)
            return send_from_directory(static_path, path)

        # register all CSS files with app
        for css_path in self.all_css_files:
            full_css_path = self._get_asset_path(css_path) 
            self.app.css.append_css({"external_url": full_css_path})

        # register all JS files with app
        for js_path in self.all_js_files:
            full_js_path = self._get_asset_path(js_path) 
            self.app.scripts.append_script({"external_url": full_js_path})

    def _register_routes(self):
        self.routes = {}
        for page in self.page_list:
            # register long route: eg /the-page-name, /another-page
            route = self._register_route(page.url, page.layout)
            # update the page url in case it was assigned a different route 
            page.url = route
            # register short route: eg /1, /2, /3
            self._register_route(f'/{str(page.index)}', page.layout)

        self._set_index_route()
            
    def _register_route(self, route, layout):
        if route in self.routes:
            suffix = ''.join(random.choices(string.ascii_letters, k=5))
            route = f'{route}-{suffix}'
        self.routes[route] = layout
        return route

    def _set_index_route(self):
        # if index_layout is specified, then we use this for the index page
        # of the story. otherwise, a layout is created according to the value 
        # of config.index_page_type
        if self.index_page_type == 'first':
            self.index_page_layout = self.page_list[0].layout
        elif self.index_page_type == 'outline':
            # TODO
            pass
        elif self.index_page_type == 'vertical':
            # TODO
            pass
        else:
            msg = "'index_page_type' param must be one of {}"
            raise ValidationException(msg.format("'first', 'outline', or 'vertical'"))
        self._register_route('/', self.index_page_layout)
            
    def _get_layout(self):
        # where should this go??
        def nav_li(href, text, active=False):
            className = 'nav-item nav-link' + (' active' if active else '')
            return html.Li(dcc.Link(text, href=href), className=className)

        navbar = html.Nav(
            className='',
            children=html.Ul(
                className='nav nav-pills',
                children=[nav_li(href, text) for href, text in self.nav_items]
            )
        )

        layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(
                id='main',
                children=[
                    html.Div(navbar, id=config.NAVBAR_ELEMENT_ID),
                    html.Div(id=config.PAGE_ELEMENT_ID)
                ]
            )
        ])

        return layout
        
    def _get_asset_path(self, path):
        if path.startswith('http'):
            return path
        return '{}/{}'.format(self.app.server.static_url_path.rstrip('/'), path)

    @property
    def xplore_base_path(self):
        """Returns the path to the directory of the Xplore package"""
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def project_path(self):
        """The path to the directory containing the user's Xplorable instance"""
        class_path = os.path.abspath(inspect.getfile(self.__class__))
        return os.path.dirname(class_path)

    @property
    def all_css_files(self):
        # returns a generator yielding all CSS files attached to pages used in
        # this story as well as those attached to this story
        pages_css = (page.all_css_files for page in self.page_list)

        return chain(
            config.CSS_FILES,
            self.__class__.css_files,
            *pages_css
        )

    @property
    def all_js_files(self):
        # returns a generator yielding all JS files attached to pages used in
        # this story as well as those attached to this story.  make sure user
        # files come last!
        pages_js = (page.all_js_files for page in self.page_list)

        return chain(
            config.JS_FILES,
            self.__class__.js_files,
            *pages_js
        )

    @property
    def nav_items(self):
        return [(page.url, page.name) for page in self.page_list]

    def __call__(self, *args):
        # This makes it so that this object can be a WSGI app target
        return self.app.server(*args)
        
