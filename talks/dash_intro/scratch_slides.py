class OldR(Block):
    name = "R?" 
    shape = [[8, 4]]
    row_classes = [['center-y']]
    content = [
        Div(Markdown("# Shiny!"), className='center-x center-y'),
        Div([
            one_col_row(Img(src='/static/img/r.svg', style={'width':'40%'})),
            one_col_row(Img(src='/static/img/shiny.png', style={'width':'70%'})),
        ], className='center pad-y-extra')
    ]
