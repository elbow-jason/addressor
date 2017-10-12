import re

from piper import categories
from piper.utils import tag_category

PREFIXES = [
    "A.P.N.:",
    "parcel no.",
    "APN #:",
    "APN #",
    "APN",
]

EXAMPLES = [
    "APN 141-36-292"
]

LABEL = categories.LABELS[categories.PARCEL_NUMBER]

APN_PATTERN = "a\.?p\.?n\.?\s?#?:?"
KEY_PATTERN = "\d{3}-\d{2}-\d{3}"
PARCEL_PATTERN = "(parcel\s+(no\.?|number|#):?)"

KEY_REGEX = re.compile(KEY_PATTERN)
APN_REGEX = re.compile(APN_PATTERN + "\s+" + KEY_PATTERN)
PARCEL_NUM_REGEX = re.compile(PARCEL_PATTERN + "\s+" + KEY_PATTERN)


def findall(text):
    lowered = text.lower()
    found = []
    found += APN_REGEX.findall(lowered)
    found += PARCEL_NUM_REGEX.findall(lowered)
    return found

def matches(text):
    return len(findall(text)) > 0

def extract(texts):
    found = []
    for text in texts:
        found += KEY_REGEX.findall(text)
    return found

def filter_categorized(texts):
    kept = []
    for text in texts:
        if isinstance(text, tuple) and text[1] in [categories.PARCEL_NUMBER, LABEL]:
            kept.append(text[0])
    return kept


class ParcelNumberPipe(object):
    def predict(self, texts):
        categorized = []
        for item in texts:
            if matches(item):
                categorized.append(categories.PARCEL_NUMBER)
            else:
                categorized.append(categories.NOTHING)
        return categorized

def generate_pipe():
    return ParcelNumberPipe()