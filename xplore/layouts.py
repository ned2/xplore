from dash_html_components import *
from dash_core_components import *

from .exceptions import ValidationException


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
    return Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=P('Next', id='next-page')
        ),
    )


def one_col_row(id_start=1):
    return Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=Div(id='content-1')
        ),
    )


def two_col_row(id_start=1):
    return Div(
        className='row',
        children=[
            Div(
                className='col-lg-6',
                children=Div(id='content-1')
            ),
            Div(
                className='col-lg-6',
                children=Div(id='content-2')
            ),
        ]
    )


def three_col_row(id_start=1):
    return Div(
        className='row',
        children=[
            Div(
                className='col-lg-4',
                children=Div(id='content-1')
            ),
            Div(
                className='col-lg-4',
                children=Div(id='content-2')
            ),
            Div(
                className='col-lg-4',
                children=Div(id='content-3')
            ),
        ]
    )


def four_col_row(id_start=1):
    return Div(
        className='row',
        children=[
            Div(
                className='col-lg-3',
                children=Div(id='content-1')
            ),
            Div(
                className='col-lg-3',
                children=Div(id='content-2')
            ),
            Div(
                className='col-lg-3',
                children=Div(id='content-3')
            ),
            Div(
                className='col-lg-3',
                children=Div(id='content-4')
            ),
        ]
    )


def six_col_row(id_start=1):
    return Div(
        className='row',
        children=[
            Div(
                className='col-lg-2',
                children=Div(id='content-1')
            ),
            Div(
                className='col-lg-2',
                children=Div(id='content-2')
            ),
            Div(
                className='col-lg-2',
                children=Div(id='content-3')
            ),
            Div(
                className='col-lg-2',
                children=Div(id='content-4')
            ),
            Div(
                className='col-lg-2',
                children=Div(id='content-5')
            ),
            Div(
                className='col-lg-2',
                children=Div(id='content-6')
            ),
        ]
    )


def row_old(ncols=1):
    col_map = {
        1: one_col_row,
        2: two_col_row,
        3: three_col_row,
        4: four_col_row,
        6: six_col_row,
        12: twelve_col_row,        
    }
    if ncols not in col_map:
        msg = "Valid values for 'ncols' param are: " \
              "{}".format(", ".join(col_map))
        raise ValidationException(msg)
    return col_map[ncols]()


def row(ncols=1, start_id=1):
    valid_cols = {1,2,3,4,6,12}
    if ncols not in valid_cols:
        msg = "Valid values for 'ncols' param are: " \
              "{}".format(", ".join(valid_cols))
        raise ValidationException(msg)
        
    cols = []
    for i in range(ncols):
        col_class = 'col-lg-{}'.format(12//ncols)
        content_id = start_id + i  
        col = Div(
            className=col_class,
            children=Div(id='content-{}'.format(content_id))
        )
        cols.append(col)
    return Div(className='row', children=cols)


def page(rows=None, header=True):
    if rows is None:
        # default to one row with a single column
        rows = [1]

    if header:
        row_list = [header_row()]
    else:
        row_list = []

    for i, ncols in enumerate(rows):
        start_id = sum(rows[:i]) + 1
        row_list.append(row(ncols, start_id=start_id))

    return Div(row_list)


def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
