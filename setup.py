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
)
