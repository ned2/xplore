import dash_html_components as html
from dash.development.base_component import Component

from .utils import add_content
from .exceptions import ValidationException


VALID_COLS = set(list(range(1,13))+[None])


def add_class(className, args_dict):
    if 'className' in args_dict:
        args_dict['className'] = f'{className} {args_dict["className"]}'
    else:
        args_dict['className'] = className

        
def add_base_styles(styles, args_dict):
    if 'style' in args_dict:
        styles.update(args_dict['style'])
    args_dict['style'] = styles 


def FontA(name):
    return html.I(className=f"fa {name}")


def Box(children=None, center=False, **kwargs):
    styles = {}
    if center:
        styles['textAlign'] = 'center'
        
    add_base_styles(styles, kwargs)
    add_class('box', kwargs)
    return html.Div(
        children=children,
        **kwargs
    )


def BackgroundImage(children=None, src=None, **kwargs):
    return html.Div(
        children=children,
        style={
            'background': f'url("/static/img/{src}") no-repeat center center fixed',
            'backgroundSize': 'cover',
            'position': 'fixed',
            'height': '100vh',
            'width': '100vw',
            'top':0,
            'zIndex':-1000
        },
        **kwargs)


def Image(src=None, round=False, width=None, **kwargs):
    styles = {
        'width': '100%',
        'height': 'auto',
    }

    if round:
        styles['border-radius'] = '10px'
    if width is not None:
        if isinstance(width, int) or (isinstance(width, str) and width.isdigit()): 
            styles['width'] = f'{width}%'
        elif isinstance(width, str):
            styles['width'] = width
        else:
            raise ValidationException("'width' must be an integer or a string")    
        
    add_base_styles(styles, kwargs)
    return html.Img(src=f'/static/img/{src}', **kwargs)


def Col(children=None, size=12, **kwargs):
    if size is None:
        col_class = 'col'
    else:
        col_class = f'col-{size}'
    add_class(col_class, kwargs)
    return html.Div(children=children, **kwargs)


def Row(content=None, shape=None, start_id=1, hcenter=False, col_classes=None, **kwargs):
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

    if col_classes is None:
        col_classes = []

    if hcenter:
        col_classes.append('d-flex')
        col_classes.append('justify-content-center')

    col_list = []
    for i, size in enumerate(shape):
        # note that we intentionally embed the content-id one extra div so
        # that we can use these IDs as temporary identifiers that can be
        # destructively removed (ie layout['some-id'] = component rather
        # than layout['some-id'].children = component) when building up
        # intermediate layout components
        content_id = start_id + i
        col = Col(
            size=size,
            children=html.Div(id=f'content-{content_id}'),
            className=' '.join(col_classes if col_classes else [])
        )
        col_list.append(col)

    kwargs['children'] = col_list
    add_class('row', kwargs)        
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

    return html.Div([prev_link, next_link], **kwargs)
