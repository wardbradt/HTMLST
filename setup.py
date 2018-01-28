from setuptools import setup

setup(
    name='htmlst',
    version='0.1.0b1',
    description='An API which extracts sentences from HTML',
    url='https://github.com/wardbradt/HTMLST',
    author='Ward Bradt',
    keywords='nlp machinelearning development',
    packages=['htmlst'],
    install_requires=['nltk', 'html5lib'],
)
