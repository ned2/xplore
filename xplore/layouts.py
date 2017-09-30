from dash_html_components import *
from dash_core_components import *
from dash.development.base_component import Component

from .exceptions import ValidationException
from .components import Col, Row
from .utils import add_content
from . import settings

# TODO:
# Warning when number of columns in shape does not much number in content

# TODO:
# push all helper functions into a sub module of layouts such that
# from xplore.layouts import * will get you only things you might want to use


# TODO need to sort out how this interfaces with Xplorable
def main(nav_items=None):
    layout = Div([
        Location(id='url', refresh=False),
        Div(
            id='main',
            children=[
                Div(id=settings.NAVBAR_ELEMENT_ID),
                Div(id=settings.PAGE_ELEMENT_ID)
            ]
        )
    ])

    if nav_items is not None:
        nav_layout = navbar(nav_items)
        layout[settings.NAVBAR_ELEMENT_ID].children = nav_layout

    return layout


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


def left_right_nav(left=None, right=None, **kwargs):
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

    row = Row([prev_link, next_link], **kwargs)
    return row


def make_block_layout(content=None, shape=None, header=True, nav_links=True,
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
        nav_links = left_right_nav(id='nav-links')
        row_list.append(nav_links)

    if header:
        row_list.append(Row(H1(id='title')))

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
    new_page = Div(row_list)

    # TODO add_content should probably be a decorator?
    if content is not None:
        add_content(new_page, content)

    return new_page


def link(href, text):
    return Link(A(text, href=href), href=href, className='link')


def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
