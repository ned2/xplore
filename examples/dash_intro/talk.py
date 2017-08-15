from xplore.story import Story

from slides import *

# Possible dash bug:
# -- img with no 'src' attribute specified seems to be triggering the
#    URL callback with a pathname of None
# -- also Img with a 'style' attr that is a string instead of a dict


# Various issues:
# 
# I am automatically prefixing static dir for CSS and JS urls but not for
# images.



# TODO
# -- create javascript file to include that binds back and forwards
#    keys to previous next link (also 'h' for home?) 
# -- create default light and dark themes


class DashTalk(Story):
    title = "Creating Reactive Web Apps in Python"
    css_files = ['css/talk.css']
    js_files = []

    pages = [
        Title, 
        Context,
    ]


talk = DashTalk()

if __name__ == '__main__':
    talk.app.server.run(debug=True)
