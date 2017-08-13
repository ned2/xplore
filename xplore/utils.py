import re


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
