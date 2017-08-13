import dash_html_components as html
import dash_core_components as dcc


def nav_li(href, text, active=False):
    return html.Li(
        className='nav-item' + (' active' if active else ''),
        children=dcc.Link(
            className='link',
            href=href,
            children=html.A(
                text,
                className='nav-link',
                href=href,
            )
        )
    )


def navbar(navbar_items):
    lis = [nav_li(href, text) for href, text in navbar_items]
    layout = html.Nav(
        className='',
        children=html.Ul(lis, className='nav nav-pills'),
    )
    return layout


def main():
    layout =html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(
            id='main',
            children=[
                html.Div(id='navbar'),
                html.Div(id='page')
            ]
        )
    ])
    return layout


def url_not_found(pathname):
    return html.P("No page '{}'".format(pathname))
