from dash_html_components import *
from dash_core_components import *


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


one_col_page = Div([
    Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=H1(id='title')
        ),
    ),
    Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=Div(id='content')
        ),
    ),
    Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=P('Next', id='next-page')
        ),
    )
])          


two_col_page = Div([
    Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=H1(id='title')
        ),
    ),
    Div(
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
    ),
    Div(
        className='row',
        children=Div(
            className='col-lg-12',
            children=P('Next', id='next-page')
        ),
    )
])



def page_not_found(pathname):
    return P("No page '{}'".format(pathname))
