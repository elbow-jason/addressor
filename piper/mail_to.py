
import re

from piper import (
    escrow_number,
    categories,
    strings,
)
from piper.utils import tag_category

PREFIXES = [
    "when recorded mail to:",
]

SUFFIXES = [
     "SPECIAL WARRANTY DEED",
     "WARRANTY DEED",
] + escrow_number.PREFIXES

UNWANTED_REGEXES = [
    re.compile("escrow"),
    re.compile("space above"),
    re.compile("recorders use"),
]

KEY_PHRASE = "when recorded mail to:"

LABEL = categories.LABELS[categories.MAIL_TO]

def find_lines(lines, size=5):
    found = []
    if len(lines) <= size:
        size = len(lines)
    for i in range(len(lines) - size):
        chunk = lines[i:i+size]
        if matches_key_phrase(chunk[0]):
            found.append(chunk)
    return found

def extract(found_lines):
    kept = found_lines
    for item in PREFIXES:
        kept = keep_non_matching_fuzzy(kept, item)
    for item in SUFFIXES:
        kept = keep_non_matching_fuzzy(kept, item)
    for regex in UNWANTED_REGEXES:
        kept = keep_non_matching_regex(kept, regex)
    return {
        "name": kept[:1],
        "address": kept[1:],
    }

def inspect(items):
    return items

def fuzzy_matches(a, b):
    return strings.similarity(a.lower(), b.lower()) >= 0.85

def regex_matches(string, regex):
    return len(regex.findall(string.lower())) > 0

def keep_non_matching_fuzzy(lines, term):
    return [line for line in lines if not fuzzy_matches(line, term)]

def keep_non_matching_regex(lines, regex):
    return [line for line in lines if not regex_matches(line, regex)]

def matches_key_phrase(text):
    return fuzzy_matches(KEY_PHRASE, text)

def filter_categorized(texts):
    kept = []
    for text in texts:
        if isinstance(text, tuple) and text[1] in [categories.MAIL_TO, LABEL]:
            kept.append(text[0])
    return kept


class MailToPipe(object):
    def predict(self, lines):
        categorized = []
        for item in lines:
            if matches(item):
                categorized.append(categories.MAIL_TO)
            else:
                categorized.append(categories.NOTHING)
        return categorized

def generate_pipe():
    return MailToPipe()