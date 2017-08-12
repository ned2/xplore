from flask import Flask, send_from_directory, redirect

from itertools import chain

import settings

class Story:

    css_files = []
    js_files = []

    # index options:
    #   'outline'  
    #   'first'
    #   'page'
    def __init__(self, app=None, layout=None,
                 index_page_type=settings.INDEX_PAGE_TYPE,
                 static_file_path=settings.STATIC_FILE_PATH):
        if app is None:
            server = Flask(__name__)
            self.app = Dash(__name__, server=server)

        self.app = app
        self.static_file_path = static_file_path 
        self.index_page_type = index_page_type
        self._init_app()
        self._validate_attrs()

        if self.index_layout is None:
            # TODO create layout of index page
        else:
            
        
    def _init_app(self):
        self.app.title = self.title
        
        # Dash complains about callbacks on nonexistent elements otherwise
        self.app.config.supress_callback_exceptions = True

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
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = {}
            for page in self.page_list:
                self._urls[page.url] = page.layout
                self._urls[page.index] = page.layout
        return self._urls

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
