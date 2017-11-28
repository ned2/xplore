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
        Need,
        WebPlatform,
        Madness,
        Glue,
        WeWant,
        Dash,
        Meta,
        DashExample,
        DashArchitecture,
        HelloWorld,
        ReactiveHelloWorld,
        UnpackingThings,
        DashArchitecture,
        Layouts,
        MiscComponents,
        DataTableComponentImage,
        #DataTableComponent,
        TabsComponent,
        MarkdownComponent,
        Extensible,
        Callbacks,
        DataStructures,
        SinglePageApps,
        Deployment,
        Limitations,
        Conclusion,
    ]


talk = DashTalk()


if __name__ == '__main__':
    talk.app.server.run(debug=True, host='0.0.0.0', port=5002)
