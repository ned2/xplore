from collections import Mapping, Iterable

from dash_html_components import *
from dash_core_components import *
from dash.development.base_component import Component

from .exceptions import ValidationException


# TODO:
# push all helper functions into a sub module of layouts such that
# from xplore.layouts import * will get you only things you might want to use


VALID_COLS = set(range(1,13))


def main():
    layout = Div([
        Location(id='url', refresh=False),
        Div(
            id='main',
            children=[
                Div(id='navbar'),
                Div(id='page')
            ]
        )
    ])
    return layout


def _make_row(cols=None, content=None, start_id=1):
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

    row = Div(className='row', children=col_list)

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
    

def make_block_layout(shape=None, content=None, header=True):
    if shape is None:
        # default to one row with a single column
        shape = [[12]]

    if header:
        row_list = [one_col_row(H1(id='title'))]
    else:
        row_list = []

    start_id = 1
    for row_cols in shape:
        row_list.append(_make_row(cols=row_cols, start_id=start_id))
        start_id += len(row_cols)

    # add the next page link
    row_list.append(one_col_row(P('Next', id='next-page')))

    # the page of rows
    new_page = Div(row_list)

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


def one_col_row(content):
    return _make_row(cols=[12], content=content)


def two_col_row(content):
    return _make_row(cols=[6, 6], content=content)


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
