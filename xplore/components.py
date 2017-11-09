import dash_html_components as html
from dash.development.base_component import Component

from .utils import add_content

VALID_COLS = set(range(1,13))


def Col(size=12, **kwargs):
    if 'className' in kwargs:
        kwargs['className'] = f'col-lg-{size} {kwargs["className"]}'
    else:
        kwargs['className'] = f'col-lg-{size}'
    return html.Div(**kwargs)


def Row(content=None, shape=None, start_id=1, **kwargs):
    if shape is None:
        if content is None or isinstance(content, Component):
            shape = [12]
        else: 
            content_len = len(content)
            if 12 % content_len != 0:
                msg = "length of 'content' param must be a factor of 12"
                raise ValidationException(msg)

            size = int(12/content_len)
            shape = [size] * content_len
            
    bad_cols = [col for col in shape if col not in VALID_COLS]
    if bad_cols:
        msg = "Invalid column value(s): {}. Valid column values are: {}"
        msg = msg.format(bad_cols, VALID_COLS)
        raise ValidationException(msg)

    col_list = []    
    for i, size in enumerate(shape):
        # note that we intentionally embed the content-id one extra div so
        # that we can use these IDs as temporary identifiers that can be
        # destructively removed (ie layout['some-id'] = component rather
        # than layout['some-id'].children = component) when building up
        # intermediate layout components
        content_id = start_id + i
        col = Col(size=size, children=html.Div(id=f'content-{content_id}'))
        col_list.append(col)

    kwargs['children'] = col_list
        
    if 'className' in kwargs:
        kwargs['className'] = f'row {kwargs["className"]}'
    else:
        kwargs['className'] = 'row'

    row = html.Div(**kwargs)

    if content is not None:
        add_content(row, content)

    return row


def Link(href, text, **kwargs):
    return html.Link(A(text, href=href), href=href, className='link', **kwargs)


def left_right_nav(left=None, right=None, **kwargs):
    next_link = html.Div(left, id='next-page')
    prev_link = html.Div(right, id='prev-page')

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
