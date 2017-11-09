from itertools import chain

import dash_core_components as dcc
import dash_html_components as html

from .utils import slugify, camel_case_to_title, add_content
from .exceptions import ValidationException
from .components import Row, Col, left_right_nav

# note: current gotcha with Block class is that layout trees in content
# attribute will be shared across all instances of the class becuase
# content is a class attribute 
# workaround1 -- define content as @property method
# workaround2 -- create deep copy of the content layout on creation of
#                each instance.
# both seem suboptimal

# another issue:
# currently Block class can't really be instantiated manually, only in the context
# of Xplorable, due to dependence on app and index params
# -- reassess


class Block:

    css_files = []
    js_files = []
    
    def __init__(self, app, index, project_path, name=None, url=None):
        self.app = app
        self.index = index

        # TODO -- this is an ugly hack
        self.project_path = project_path
        
        if name is not None:
            self._name = name

        if url is not None:
            self._url = url

        if hasattr(self, 'get_data'):
            self.get_data()

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
            if not hasattr(self, 'row_classes'):
                self.row_classes = None
            layout = self._make_layout(
                shape=self.shape,
                content=self.content,
                row_classes=self.row_classes,
            )
        else:
            msg = "Block subclasses must either define a 'layout' attribute, " \
                  "a 'get_layout' method, or both 'shape' and 'content' attributes."
            raise ValidationException(msg)
        return layout

    # TODO: fix this function call, then test moved around code
    def _make_layout(self, content=None, shape=None, header=True, nav_links=True,
                          row_classes=None):

        # TODO:
        # Warning when number of columns in shape does not much number in content

        if shape is None:
            # default to one row with a single column
            shape = [[12]]

        if row_classes is None:
            row_classes = [[] for _ in range(len(shape))]
        elif len(row_classes) != len(shape):
            msg = "'row_classes' param must be the same length as 'shape' param" 
            raise ValidationException(msg)

        row_list = []

        if nav_links:
            nav_links = left_right_nav(id='nav-links')
            row_list.append(nav_links)

        if header:
            row_list.append(Row(html.H1(id='title')))

        start_id = 1
        for i, row_shape in enumerate(shape):
            row = Row(
                shape=row_shape,
                start_id=start_id,
                className=row_classes[i]
            )
            row_list.append(row)
            start_id += len(row_shape)

        # the page of rows
        layout = html.Div(row_list)

        # TODO add_content should probably be a decorator?
        if content is not None:
            add_content(layout, content)

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
            self._url = f'/{slugify(self.name)}'
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        
    @property
    def name(self):
        if not hasattr(self, '_name'):
            self._name = camel_case_to_title(self.__class__.__name__)
        return self._name
