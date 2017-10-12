
from faker import Faker
import random

from piper.utils import open_data_type, tag_category, get_lines
from piper.categories import ORGANIZATION, LABELS
from piper import utils
from piper.predictor import generate_pipe
from piper.preprocessing import word_tokenize

producer = Faker()

LABEL = LABELS[ORGANIZATION]

TERMS = [
    "Title Insurance Company"
    "Title",
    "Insurance",
    "Company",
    "AGENCY",
    "LLC",
    ", LLC",
    "Agency",
    "an Arizona limited liability company",
    "limited liability company",
    "L.L.C.",
    "INC.",
    "INC",
    "Investment",
    "Properties",
    "First",
    "American",
    "corporation",
    "Corporation",
]

NUM_TERMS = len(TERMS)

def random_organization():
    i = random.randrange(0, NUM_TERMS-1)
    parts = [
        producer.company(),
        TERMS[i],
    ]
    return " ".join(parts)

def new_list(limit=30000):
    return [random_organization() for i in range(limit)]

FILENAME = "./data/organizations.txt"

orgs = get_lines(FILENAME, new_list)

MAX_COUNT = len(orgs)

def get_list(limit=MAX_COUNT):
    if limit is MAX_COUNT:
        return orgs
    else:
        return random.sample(orgs, limit)

def get_categorized():
    return tag_category(ORGANIZATION, get_list())

def get_pipe():
    return generate_pipe(get_categorized())

pipe = get_pipe()

def extract(line):
    if isinstance(line, str):
        tokens = word_tokenize(line)
        return tokens
    if isinstance(line, list):
        return [extract(l) for l in line]


def filter_categorized(texts):
    kept = []
    for text in texts:
        if isinstance(text, tuple) and text[1] in [ORGANIZATION, LABEL]:
            kept.append(text[0])
    return kept
