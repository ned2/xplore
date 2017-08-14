PAGE_ELEMENT_ID = 'page'

NAVBAR_ELEMENT_ID = 'navbar'

# Possible values are:
# 'first'
# 'outline'
# 'vertical'
INDEX_PAGE_TYPE = 'first'

USE_BOOTSTRAP = True

NAVBAR = True

# Change this if you need to override Flask's default
#STATIC_FOLDER = 'static'

# Change this if you need to override Flask's default
#STATIC_URL_PATH = '/static'

# The generated routes will be prefixed with the value of STATIC_URL_PATH unless
# they begin with 'http'
BOOTSTRAP_CSS_URLS = ['xplore/css/bootstrap.min.css']

# The generated routes will be prefixed with the value of STATIC_URL_PATH unless
# they begin with 'http'
BOOTSTRAP_JS_URLS = [
    'xplore/js/jquery-3.2.1.slim.min.js',
    'xplore/js/popper.min.js',
    'xplore/js/bootstrap.min.js',
]
