import re
from collections import defaultdict, Mapping, Iterable

from dash.development.base_component import Component

from .exceptions import ValidationException


LITTLE_WORDS = {
    'the',
    'a',
    'an',
    'and',
    'in',
    'for',
    'of',
    'at',
    'around',
    'by',
    'after',
    'along',
    'from',
    'on',
    'to',
    'with',
    'without'
}


class AttrDict(defaultdict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    
def load_settings(module):
    settings = AttrDict(lambda :None)
    for setting in dir(module):
        if setting.isupper():
            settings[setting.lower()] = getattr(module, setting)
    return settings


def slugify(string):
    """
    Slugifies a string by stripping leading and trailing whitespace,
    lowercasing, stripping all non aphanumeric characters except for '-'
    and replacing sequences of whitespace with '-'.
    """
    string = re.sub(r'[^\w\s-]', '', string).strip().lower()
    string = re.sub(r'[-\s]+', '-', string)
    return string


def camel_case_split(token):
    regex = '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
    matches = re.finditer(regex, token)
    return [m.group(0) for m in matches]


def camel_case_to_title(token):
    words = camel_case_split(token)
    new_words = []
    for i, word in enumerate(words):
        if i == 0 or i == len(words)-1:
            new_words.append(word)
            continue
        if word.lower() in LITTLE_WORDS:
            new_words.append(word.lower())
        else:
            new_words.append(word)
    return " ".join(new_words)


def add_content(layout, content):
    # note that we always replace the content-ID element
    # to reduce chance of collisions later

    if isinstance(content, Component):
        # content is a single Dash Component
        layout['content-1'] = content
    elif isinstance(content, Mapping):
        # content is a dict-like object with element-ID keys and components as
        # values
        for id_name, value in content.items():
            layout[id_name] = value
    elif isinstance(content, Iterable):
        # content is an iterable
        for i, value in enumerate(content):
            layout['content-{}'.format(i+1)] = value
    else:
        msgs = "'content' param must be a dict-like object, iterable, " \
               "or Dash Component"
        raise ValidationException(msg)
