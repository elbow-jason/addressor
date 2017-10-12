import re

from nltk import tokenize

MULTINEWLINES = re.compile("\n{2,}")

SYMBOLS = {
    ",",
    "}",
    "{",
    "`",
    "\'",
    "‘",
    "`",
}


def only_valid_chars(text):
    return re.sub('[^A-Za-z0-9-\s]+', '', text)


def remove_symbols(text):
    new_text = ""
    for letter in text:
        if letter not in SYMBOLS:
            new_text += letter
    return new_text

def tilde_to_dash(text):
    return text.replace("~", "-")

def clean(text):
    text = tilde_to_dash(text)
    # text = remove_symbols(text)
    text = only_valid_chars(text)
    return text

def into_sections(text):
    return [" ".join(x.strip().split()) for x in MULTINEWLINES.split(text)]


def remove_empties(texts):
    return [x for x in texts if len(x) > 0]

def word_tokenize(text):
    return tokenize.word_tokenize(text)

def to_lines(text):
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 0:
            lines.append(line)
    return lines


def to_word_chunks(text, size=14):
    tokens = word_tokenize(text)
    upper_limit = len(tokens) - size
    if upper_limit <= 0:
        return [" ".join(tokens)]
    chunked = []
    for i in range(upper_limit):
        chunked.append(" ".join(tokens[i:i+size]))
    return chunked
    