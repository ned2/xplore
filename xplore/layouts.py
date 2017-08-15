from collections import Mapping, Iterable

from dash_html_components import *
from dash_core_components import *
from dash.development.base_component import Component

from .exceptions import ValidationException

VALID_COLS = set(range(1,13))


def main():
    layout =Div([
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


def make_row(cols=None, start_id=1):
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
        col = Div(
            id='content-{}'.format(content_id),
            className=col_class,
        )
        col_list.append(col)
    return Div(className='row', children=col_list)


def make_page_layout(shape=None, header=True, content=None):
    if shape is None:
        # default to one row with a single column
        shape = [[12]]

    if header:
        row_list = [header_row()]
    else:
        row_list = []

    start_id = 1
    for row_cols in shape:
        row_list.append(make_row(cols=row_cols, start_id=start_id))
        start_id += len(row_cols)
    row_list.append(next_page_row())

    # the page of rows
    new_page = Div(row_list)

    if content is not None:
        # content is a single Dash Component
        if isinstance(content, Component):
            new_page['content-1'].children = content
        # content is a dict-like object with element-ID keys and components as
        # values
        elif isinstance(content, Mapping):
            for id_name, value in content.items():
                new_page[id_name].children = value
        elif isinstance(content, Iterable):
            # content is a dict-like object with element-ID keys and components as
            # values
            for i, value in enumerate(content):
                new_page['content-{}'.format(i+1)].children = value
        else:
            msgs = "'content' param must be a dict-like object, iterable, " \
                   "or Dash Component"
            raise ValidationException(msg)
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


def header_row():
    return Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=H1(id='title')
        ),
    )


def next_page_row():
    row = one_col_row()
    row['content-1'] = P('Next', id='next-page')
    return row


def one_col_row(start_id=1):
    return make_row(cols=[12], start_id=start_id)


def two_col_row(start_id=1):
    return make_row(cols=[6, 6], start_id=start_id)


def three_col_row(start_id=1):
    return make_row(cols=[4, 4, 4], start_id=start_id)


def four_col_row(start_id=1):
    return make_row(cols=[3, 3, 3, 3], start_id=start_id)


def six_col_row(start_id=1):
    return make_row(cols=[2, 2, 2, 2, 2, 2], start_id=start_id)

def tweleve_col_row(start_id=1):
    return make_row(cols=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], start_id=start_id)


def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
