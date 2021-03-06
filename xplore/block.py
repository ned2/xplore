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
    shape = [[12]]
    header = False
    title = False
    hcenter = True
    vcenter = True
    row_vcenter = True
    row_classes = None
    row_heights = None
    
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

        layout = self._make_layout()
        return layout

    def _make_layout(self):
        container = self._make_container()
        layout = [left_right_nav(id='nav-links')]

        if self.header:
            layout.append(html.H1(
                id="header",
                children=self.name,
                style={'height':'10vh'}
            ))
            container.style = {'height':'90vh'}

        layout.append(container)
        return html.Div(layout)
    
    def _make_container(self):
        if self.row_classes is not None and len(self.row_classes) != len(self.shape):
            msg = "'row_classes' param must be the same length as 'shape' param" 
            raise ValidationException(msg)

        if self.row_heights is not None and len(self.row_heights) != len(self.shape):
            msg = "'row_heights' param must be the same length as 'shape' param" 
            raise ValidationException(msg)

        row_list = []

        if self.title:
            row_list.append(Row(html.H1(id='title', children=self.name)))

        start_id = 1
        for i, row_shape in enumerate(self.shape):        
            row_classes, col_classes = [], []
            if self.row_vcenter:
                row_classes.append('align-items-center')
            if self.hcenter:
                row_classes.append('justify-content-center')
                
            if self.row_classes is not None:
                row_classes.append(self.row_classes[i])

            if self.row_heights is not None and self.row_heights[i] is not None:
                style = {'height': f'{self.row_heights[i]}vh'}
            else:
                style = {}

            row_list.append(Row(
                shape=row_shape,
                start_id=start_id,
                col_classes=col_classes,
                hcenter=self.hcenter,
                className=' '.join(row_classes),
                style=style,
                
            ))
            start_id += len(row_shape)

        container_classes = ['container-fluid']

        if self.vcenter:
            container_classes.append('d-flex align-items-center')
        if self.hcenter:
            container_classes.append('justify-content-center')
            
        # the bootstrap container    
        container = html.Div(
            id="content",
            className=' '.join(container_classes),
            children=html.Div(row_list)
        )

        if hasattr(self, 'content'):
            if isinstance(self.content, list):
                num_elements = len(list(chain.from_iterable(self.shape)))
                if num_elements != len(self.content):
                    msg = "'shape' param must have same number elements as 'content' param" 
                    raise ValidationException(msg)
            add_content(container, self.content)

        return container
    
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
