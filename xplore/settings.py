PAGE_ELEMENT_ID = 'page'

NAVBAR_ELEMENT_ID = 'navbar'

# Possible values are:
# 'first'
# 'outline'
# 'vertical'
INDEX_PAGE_TYPE = 'first'

USE_BOOTSTRAP = True

# does not work as expected currently
SERVE_LOCALLY = False

NAVBAR = True

# path of static files relative to your project root 
STATIC_FOLDER = 'static'

# Change this if you need to override Flask's default
#STATIC_URL_PATH = '/static'

# change BOOTSTRAP_CSS_URLS and BOOTSTRAP_JS_URLS if you want to use a different
# version of bootstrap from the one that comes with xplore (v4.0.0 beta) The
# generated routes will be prefixed with the value of STATIC_URL_PATH unless
# they begin with 'http'
BOOTSTRAP_CSS_URLS = ['xplore/css/bootstrap.min.css']
BOOTSTRAP_JS_URLS = [
    'xplore/js/jquery-3.2.1.slim.min.js',
    'xplore/js/popper.min.js',
    'xplore/js/bootstrap.min.js',
]
