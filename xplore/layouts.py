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


def page(rows=None, header=True, content=None):
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

    row_list.append(next_page_row())

    # the page of rows
    new_page = Div(row_list)

    if content is not None:
        for id_name, value in content.items():
            new_page[id_name] = value
            
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
    return row(ncols=1, start_id=start_id)


def two_col_row(start_id=1):
    return row(ncols=2, start_id=start_id)


def three_col_row(start_id=1):
    return row(ncols=3, start_id=start_id)


def four_col_row(start_id=1):
    return row(ncols=4, start_id=start_id)


def six_col_row(start_id=1):
    return row(ncols=6, start_id=start_id)


def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
