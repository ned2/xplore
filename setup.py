from setuptools import setup, find_packages

setup(
    name='xplore',
    version='0.1',
    py_modules=['xplore'],
    license='MIT',
    install_requires=[
        'dash',
        'flask',
        'dash_html_components',
        'dash_core_components',        
    ],
    packages=find_packages(),
    package_data={'xplore': ['static']},
    classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 1 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Manufacturing',
    'Intended Audience :: Science/Research',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Database :: Front-Ends',
    'Topic :: Office/Business :: Financial :: Spreadsheet',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Widget Sets',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.5',
],
)
