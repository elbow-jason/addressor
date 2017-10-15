import random
import re

import usaddress

from piper.utils import open_data_type, tag_category
from piper.categories import STRICT_ADDRESS
from piper import utils
from piper.predictor import generate_pipe
from piper.preprocessing import word_tokenize

FILENAME = "./data/addresses.txt"

with open(FILENAME, "r") as f:
    addresses = [x.strip() for x in f.readlines()]

MAX_COUNT = len(addresses)

def get_list(limit=MAX_COUNT):
    if limit is MAX_COUNT:
        return addresses
    else:
        return random.sample(addresses, limit)

def get_categorized():
    return tag_category(STRICT_ADDRESS, get_list())

def get_pipe():
    return generate_pipe(get_categorized())

pipe = get_pipe()

PO_REGEX = re.compile("^p\.?o\.?&")

ADDRESS_LABELS = {
    'AddressNumber',
    'StreetNamePreDirectional',
    'StreetName',
    'StreetNamePostType',
    'PlaceName',
    'StateName',
    # 'ZipCode',
}

def extract(line):
    started = False
    parts = usaddress.parse(line)
    kept = []
    for (item, label) in parts:
        if label in ADDRESS_LABELS:
            started = True
        if label == "ZipCode" and len(item) == 5:
            # done
            kept.append(item)
            return " ".join(kept)
        if started:
            kept.append(item)
    return ""

# def deduplicate_substrings(strings):
#     deduped = []
#     for string in strings:
#         if not string in deduped:
#             deduped.append(string)
#     sorted_strings = sorted(deduped, key=lambda item: 0-len(item))
#     keepers = sorted_strings[:1]
#     for string in sorted_strings[1:]:
#         for keeper in keepers:
#             if string not in keeper:
#                 keepers.append(string)
#     return keepers

# BELOW ARE THE NEW PARTS

PREFIXES = [
    "ADDRESS:",
    "Property Address"
]

SUFFIXES = [
    "'File No.",
]