import sys
import os
import importlib
import inspect
from itertools import chain
from collections import Mapping

from dash import Dash
from dash.dependencies import Input, Output
from dash.development.base_component import Component
from flask import Flask, send_from_directory

from . import layouts, utils
from .exceptions import ValidationException

# TODO: A bug:
# when two slides have the same name their generates routes clash


# Grand plan:
#
# content params should be able to take pages as values. This means that the
# Page class should be called something else 'Block' maybe?
#
# Story subclasses should take a param multi_page. if True, each Block specified
# in content is an independent page with generated routes. if False, content is
# laid out according to 'shape', just like in Block class. 

# This will mean that the ID for each block will need to have an index
# change page ID setting to something like BLOCK_ID_PREFIX = 'block

# Other ideas:

# Implement themes/addons as Mixins which introduce specific functionality
# eg PresentationMixin which adds css and js required to turn into a talk.
# probably include chevrons is css? also sets multi-page to True 

# 'app' attribute on Xplorable should be 'dash'??
# to help stop people thinking its the Flask app
# -- on the other hand, all the dash docs refer to the Dash instance as 'app'

# not sure about this one
# should Story class just be a Block?? and have it be blocks all the way down??
# while perhaps might be able to be made to work, there will be attributes that
# are specific to the whole app but not individual blocks. eg multi_page

# Xplorable takes a param:
# routes = {name, number, both}
# generates routes for pages according to respective values

# as it stands I think maybe I've somewhat coupled the make_block_layout
# function to the presentation module thing. how to reconcile.
# maybe it should be part of the PresentationMixin, when it's a thing?


class Xplorable:

    css_files = [
        'xplore/css/xplore.css',
        'xplore/font/source-sans-pro/source-sans-pro.css',
    ]
    js_files = []

    # available settings that can be configured
    settings_attrs = (
        'page_element_id',
        'navbar_element_id',
        'index_page_layout',
        'index_page_type',
        'route_not_found_layout',
        'root_path',
        'serve_locally',
        'use_bootstrap',
        'bootstrap_js_urls',
        'bootstrap_css_urls',
        'navbar',
        'static_url_path',
        'static_folder',
    )

    # subset of 'settings_attrs' that should be passed onto Flask
    flask_setting_attrs = (
        'static_url_path',
        'static_folder'
    )
    
    index_page_options = (
        'outline',
        'first',
        'vertical'
    )

    # TODO
    # setting hierarchy:
    #  -- settings param

    # TODO -- add navbar orientation flag, horizontal/vertical
    def __init__(self, app=None, server=None, settings=None, **settings_kwargs):
        # load the settings
        if settings is None:
            # no settings supplied, use xplore's defaults.  TODO: a local
            # settings.py in the same directory as class inheriting from Xplorable
            # should be automatically used instead of xplore's
            settings_module = importlib.import_module('.settings', __package__)
            self.settings = utils.load_settings(settings_module)
        elif isinstance(settings, str):
            # a string containing the settings module was supplied
            # does this work?
            app_path = inspect.getfile(self.__class__)
            sys.path.append(app_path)
            settings_module = importlib.import_module(settings)
            self.settings = utils.load_settings(settings_module)
        elif isinstance(Mapping):
            # a dict-like object with settings as key-values was supplied
            self.settings = settings
        else:
            msg = "'settings' parameter must a string containing the name of " \
                  "a settings module or a dict-like object containing " \
                  "setting names and values."
            raise ValidationException(msg)

        for setting in self.settings_attrs:
            # update current settings with those specified as parameters these
            # will override any settings supplied with the 'settings' parameter
            value = settings_kwargs.get(setting, None)
            if value is not None:
                self.settings[setting] = value            

        # derive and save what is hopefully the path to the file that
        # defines the Xplorable subclass being used
        self.class_path = os.path.abspath(inspect.getfile(self.__class__))

        self._init_app(server)
        self._set_index_route()

    def _init_app(self, server):
        if server is None:
            # extract flask specific params from the settings
            flask_kwargs = {}
            for param in self.flask_setting_attrs:
                if self.settings[param] is not None:
                    flask_kwargs[param] = self.settings[param]

            # prefix the 'static_folder' param with the root of the user's project
            flask_kwargs['static_folder'] = os.path.join(
                os.path.dirname(self.class_path), 
                flask_kwargs.get('static_folder', 'static')
            )
            server = Flask(__name__, **flask_kwargs)

        self.app = Dash(name=__name__, server=server)
        self.app.title = self.title
        self.app.css.config.serve_locally = self.settings.serve_locally
        self.app.css.config.serve_locally = self.settings.serve_locally
        self.app.layout = layouts.main(self.settings, nav_items=self.nav_items)
                    
        # Dash complains about callbacks on nonexistent elements otherwise
        self.app.config.supress_callback_exceptions = True

        # register the router callback with Dash
        @self.app.callback(Output(self.settings.page_element_id, 'children'),
              [Input('url', 'pathname')])
        def display_page(pathname):
            # users can supply a default layout which can either be
            # a dash component. a callable that returns a dash layout
            if self.settings.route_not_found_layout is None:
                default_layout = layouts.page_not_found(pathname)
            elif isinstance(self.settings.route_not_found_layout, Component):
                default_layout = self.settings.route_not_found_layout
            elif callable(self.settings.route_not_found_layout):
                default_layout = self.settings.route_not_found_layout(pathname)
            else:
                # TODO raise validation error
                pass
            return self.routes.get(pathname, default_layout)
        
        # register xplore's static route with Flask
        @self.app.server.route('{}/xplore/<path:path>'.format(
            self.app.server.static_url_path))
        def send_static(path):
            static_path = os.path.join(self.xplore_base_path, 'static')
            return send_from_directory(static_path, path)

        # register all CSS files with app
        for css_path in self.all_css_files:
            full_css_path = self._get_asset_path(css_path) 
            self.app.css.append_css({"external_url": full_css_path})

        # register all JS files with app
        for js_path in self.all_js_files:
            full_js_path = self._get_asset_path(js_path) 
            self.app.scripts.append_script({"external_url": full_js_path})

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
            
    def _get_asset_path(self, path):
        if path.startswith('http'):
            return path
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

                if prev_page is not None:
                    # link this page to the last one
                    page.prev_page = prev_page
                    prev_page.next_page = page
                    
                self._page_list.append(page)
                prev_page = page

            # link the last page to the first page    
            prev_page.next_page = self._page_list[0]

            # link the first page to the last page
            self._page_list[0].prev_page = prev_page

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
                # register short route: eg /1, /2, /3
                self.register_route('/'+page.url, page.layout)

                # register long route: eg /the-page-name, /another-page
                self.register_route('/'+str(page.index), page.layout)
        return self._routes

    @property
    def all_css_files(self):
        # returns a generator yielding all CSS files attached to pages used in
        # this story as well as those attached to this story
        pages_css = (page.all_css_files for page in self.page_list)

        if self.settings.use_bootstrap:
            bootstrap_css = self.settings.bootstrap_css_urls
        else:
            bootstrap_css = []

        return chain(
            bootstrap_css,
            self.__class__.css_files,
            Xplorable.css_files,
            *pages_css
        )

    @property
    def all_js_files(self):
        # returns a generator yielding all JS files attached to pages used in
        # this story as well as those attached to this story.  make sure user
        # files come last!
        pages_js = (page.all_js_files for page in self.page_list)

        if self.settings.use_bootstrap:
            bootstrap_js = self.settings.bootstrap_js_urls
        else:
            bootstrap_js = []

        return chain(
            bootstrap_js,
            self.__class__.js_files,
            Xplorable.js_files,
            *pages_js
        )

    @property
    def nav_items(self):
        return [(page.url, page.name) for page in self.page_list]
