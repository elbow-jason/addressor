
from piper import strings

import re

PREFIXES = [
    "Escrow Number:",
    "Escrow No.",
    "RE Escrow No",
]

ESCROW_TAG_PATTERN = "(?P<tag>(re )?escrow ?(no|number|#).?:? )"
ESCROW_TAG_REGEX = re.compile(ESCROW_TAG_PATTERN)
ESCROW_REGEX = re.compile(ESCROW_TAG_PATTERN + "(?P<number>\S+)", re.IGNORECASE)

def extract_lines(lines):
    found = []
    for line in lines:
        extracted = extract(line)
        if extracted is not None:
            found.append(extracted)
    return found

def extract(line):
    matches = ESCROW_REGEX.search(line)
    if matches:
        return matches.group("number")
    return None
