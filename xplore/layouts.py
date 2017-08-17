from collections import Mapping, Iterable

from dash_html_components import *
from dash_core_components import *
from dash.development.base_component import Component

from .exceptions import ValidationException

# TODO:
# Warning when number of columns in shape does not much number in content

# TODO:
# push all helper functions into a sub module of layouts such that
# from xplore.layouts import * will get you only things you might want to use


VALID_COLS = set(range(1,13))


# TODO need to sort out how this interfaces with Xplorable
def main(settings, nav_items=None):
    layout = Div([
        Location(id='url', refresh=False),
        Div(
            id='main',
            children=[
                Div(id=settings.navbar_element_id),
                Div(id=settings.page_element_id)
            ]
        )
    ])

    if settings.navbar and nav_items is not None:
        nav_layout = navbar(nav_items)
        layout[settings.navbar_element_id].children = nav_layout

    return layout


def _make_row(cols=None, content=None, start_id=1, row_classes=None, style=None):
    # note: be careful when leaving content as None
    
    if cols is None:
        # no columns specified; make a row with a single column
        cols = [12]

    bad_cols = [col for col in cols if col not in VALID_COLS]
    if bad_cols:
        msg = "Invalid column value(s): {}. Valid column values are: {}"
        msg = msg.format(bad_cols, VALID_COLS)
        raise ValidationException(msg)

    col_list = []
    for i, col_size in enumerate(cols):
        col_class = 'col-lg-{}'.format(col_size)
        content_id = start_id + i
        # note that we intentionally embed the content-id one extra div so that
        # we can use these IDs as temporary identifiers that can be
        # destructively removed (ie layout['some-id'] = component rather than
        # layout['some-id'].children = component) when building up intermediate
        # layout components
        col = Div(
            className=col_class,
            children=Div(id='content-{}'.format(content_id)
            )
        )
        col_list.append(col)

    if row_classes is None:
        className = 'row'
    else:
        className = 'row {}'.format(' '.join(row_classes))

    row = Div(className=className, children=col_list)

    if style is not None:
        row.style = style
        
    if content is not None:
        _add_content(row, content)

    return row


def _add_content(layout, content):
    # note that we always replace the content-ID element
    # to reduce chance of collisions later

    # content is a single Dash Component
    if isinstance(content, Component):
        layout['content-1'] = content
    # content is a dict-like object with element-ID keys and components as
    # values
    elif isinstance(content, Mapping):
        for id_name, value in content.items():
            layout[id_name] = value
    elif isinstance(content, Iterable):
        # content is a dict-like object with element-ID keys and components as
        # values
        for i, value in enumerate(content):
            layout['content-{}'.format(i+1)] = value
    else:
        msgs = "'content' param must be a dict-like object, iterable, " \
               "or Dash Component"
        raise ValidationException(msg)

    
def left_right_nav(left=None, right=None):
    next_link = Div(left, id='next-page')
    prev_link = Div(right, id='prev-page')

    chevron_size = 2 # em
    chevron_area = 2*chevron_size
    shared_styles = {
        'height': '{}em'.format(chevron_area),
        'width': '{}em'.format(chevron_area),
        'backgroundRepeat': 'no-repeat',
        'backgroundSize': '{}em'.format(chevron_size),
    }

    # TODO use STATIC_URL_PATH here

    if left is None:
        prev_link.style = {
            'background': 'url(/static/xplore/svg/left_arrow.svg)',
            'backgroundPosition': 'left top',
            **shared_styles
        }

    if right is None:
        next_link.style = {
            'background': 'url(/static/xplore/svg/right_arrow.svg)',
            'backgroundPosition': 'right top',
            **shared_styles
        }

    row = two_col_row((prev_link, next_link))
    return row


def make_block_layout(shape=None, content=None, header=True, nav_links=True,
                      row_classes=None):
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
        nav_links = left_right_nav()
        nav_links.id = 'nav-links'
        # wouldn't this look nicer as left_right_nav(id='nav-links')??
        row_list.append(nav_links)

    if header:
        row_list.append(one_col_row(H1(id='title')))

    start_id = 1
    for i, row_cols in enumerate(shape):
        row = _make_row(
            cols=row_cols,
            start_id=start_id,
            row_classes=row_classes[i]
        )
        row_list.append(row)
        start_id += len(row_cols)

    # the page of rows
    new_page = Div(row_list)

    # TODO _add_content should probably be a decorator
    if content is not None:
        _add_content(new_page, content)

    return new_page


def link(href, text):
    return Link(A(text, href=href), href=href, className='link')


def nav_li(href, text, active=False):
    className = 'nav-item nav-link' + (' active' if active else ''),
    return Li(link(href, text), className=className)


def navbar(navbar_items):
    lis = [nav_li(href, text) for href, text in navbar_items]
    layout = Nav(
        className='',
        children=Ul(lis, className='nav nav-pills'),
    )
    return layout


# TODO thread **kwargs through these so that we can easily update
# attrs such as style, className etc...
# ....which kinda suggests that these should be classes and they want to
# be inheriting from a base class, so that we get all that for free???
# one possibility is that that we just go whole hog and extend from
# dash.Component. or we could have a light wrapper around component


# I think there should definitely at least be Row and Col classes

def one_col_row(content, style=None):
    return _make_row(cols=[12], content=content, style=style)


def two_col_row(content, style=None):
    return _make_row(cols=[6, 6], content=content, style=style)


def three_col_row(content):
    return _make_row(cols=[4, 4, 4], content=content)


def four_col_row(content):
    return _make_row(cols=[3, 3, 3, 3], content=content)


def six_col_row(content):
    return _make_row(cols=[2, 2, 2, 2, 2, 2], content=content)


def twelve_col_row(content):
    return _make_row(cols=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], content=content)


def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
