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

APN_PATTERN = "(?P<apn>A\.?P\.?N\.?\s?#?:?)"
KEY_PATTERN = "(?P<key>\d{3}-?\d{2}-?\d{3})"
PARCEL_PATTERN = "(?P<parcel>(parcel\s+(no\.?|number|#):?))"

KEY_REGEX = re.compile(KEY_PATTERN, re.IGNORECASE)
APN_REGEX = re.compile(APN_PATTERN + "\s+" + KEY_PATTERN, re.IGNORECASE)
PARCEL_NUM_REGEX = re.compile(PARCEL_PATTERN + "\s+" + KEY_PATTERN, re.IGNORECASE)

def extract(text):
    matched = APN_REGEX.search(text)
    if matched:
        return matched.group("key")
    return None


def extract(lines):
    kept = []
    for line in lines:
        found = APN_REGEX.search(line)
        if found:
            kept.append(found.groupdict().get("key"))
        found = PARCEL_NUM_REGEX.search(line)
        if found:
            kept.append(found.groupdict().get("key"))
    return [reformat(x) for x in kept]

def reformat(apn):
    apn = apn.replace("-", "")
    return "-".join([
        apn[:3],
        apn[3:5],
        apn[5:],
    ])

def filter_categorized(texts):
    kept = []
    for text in texts:
        if isinstance(text, tuple) and text[1] in [categories.PARCEL_NUMBER, LABEL]:
            kept.append(text[0])
    return kept


# class ParcelNumberPipe(object):
#     def predict(self, texts):
#         categorized = []
#         for item in texts:
#             if matches(item):
#                 categorized.append(categories.PARCEL_NUMBER)
#             else:
#                 categorized.append(categories.NOTHING)
#         return categorized

# def generate_pipe():
#     return ParcelNumberPipe()