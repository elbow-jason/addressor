
from faker import Faker
import random

from piper.utils import open_data_type, tag_category, get_lines
from piper.categories import LEGAL_PERSON, LABELS
from piper import utils
from piper.predictor import generate_pipe
from piper.preprocessing import word_tokenize, deduplicate_substrings

PREFIXES = [
    "Name:",
    "personally appeared",
    "hereby convey to",
    "Legal Counsel of ",
    "valuable considerations I or we"
]

SUFFIXES = [
    "unmarried man",
    "unmarried woman",
    "married woman", 
    "married man", 
    "sole and separate property",
    "personally known to me",
    "proved to me",
    "husband and wife",
    "as Joint Tenants",
    "who acknowledged the signing",
]

STOP_WORDS = {
    "grantee",
    "grantor",
    "and",
    "subject",
    "to",
    "existing",
    "beneficiary",
    "disclosure",
    "notary",
    "public",
    "trustee",
    "trust",
    "unofcial",
    "unofficial",
    "document",
    "name",
    "address",
    "agreement",
    "declaration",
    "recorded",
    "as",
    "of",
    "official",
    "records",
}

producer = Faker()

LABEL = LABELS[LEGAL_PERSON]


NUM_PREFIXES = len(PREFIXES)
NUM_SUFFIXES = len(SUFFIXES)

def random_legal_person():
    i_prefix = random.randrange(0, NUM_PREFIXES-1)
    i_suffix = random.randrange(0, NUM_SUFFIXES-1)
    parts = [
        PREFIXES[i_prefix],
        producer.name(),
        SUFFIXES[i_suffix],
    ]
    return " ".join(parts)

def new_list(limit=20000):
    return [random_legal_person() for i in range(limit)]

FILENAME = "./data/legal_person.txt"

persons = get_lines(FILENAME, new_list)

MAX_COUNT = len(persons)

def get_list(limit=MAX_COUNT):
    if limit >= MAX_COUNT:
        return persons
    else:
        return random.sample(persons, limit)

def get_categorized():
    return tag_category(LEGAL_PERSON, get_list())

def get_pipe():
    return generate_pipe(get_categorized())

pipe = get_pipe()

def extract(line):
    if isinstance(line, str):
        tokens = word_tokenize(line)
        if len(tokens) < 3:
            return []
        kept = []
        for i in range(len(tokens)-3):
            group = tokens[i:i+3]
            if group_is_a_keeper(group):
                kept.append(group)
            return [" ".join(group) for group in kept]
        else:
            return []
    if isinstance(line, list):
        items = []
        for l in line:
            items += extract(l)
        return deduplicate_substrings(items)

def group_is_a_keeper(group):
    return all(is_a_keeper(item) for item in group)

def is_a_keeper(token):
    if len(token) == 0: # empty string
        return False
    elif token[0].islower(): # not capitalized
        return False
    elif any(char.isdigit() for char in token): # has number
        return False
    elif token.lower() in STOP_WORDS: # stop_word
        return False
    return True

ALLOWED = [LEGAL_PERSON, LABEL]

def filter_categorized(texts):
    return [text for text, cat in texts if cat in ALLOWED]
