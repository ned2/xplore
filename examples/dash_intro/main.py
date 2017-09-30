from xplore import Xplorable

from slides import *


# Possible dash bug:
# -- img with no 'src' attribute specified seems to be triggering the
#    URL callback with a pathname of None
# -- also Img with a 'style' attr that is a string instead of a dict

# Various issues:
# 
# I am automatically prefixing static dir for CSS and JS urls but not for
# images specified in the layout 



class DashTalk(Xplorable):
    title = "Creating Reactive Web Apps in Python"
    css_files = [
        'css/tree.css',
        'css/dash-intro.css'
    ]
    js_files = ['js/dash-intro.js']

    pages = [
        Title, 
        Context,
        JavaScript,
        R,
        Python,
        Dash,
        DashExample,
        Architecture,
        HelloWorld,
        Layouts,
        ReactiveHelloWorld,
        Callbacks,
        LayoutsAndCallbacks,
        FeatureMarkdown,
        SinglePageApps,
        Extensible,
        Deployment,
        Limitations,
        Conclusion,
        Conclusion,
    ]


talk = DashTalk()


if __name__ == '__main__':
    talk.app.server.run(debug=True, host='0.0.0.0')
