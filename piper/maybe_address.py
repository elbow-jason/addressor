from faker import Faker
import random

from piper.utils import (
    open_data_type,
    tag_category,
    get_lines,
)
from piper.categories import MAYBE_ADDRESS
from piper.predictor import generate_pipe

producer = Faker()

FILENAME = "./data/maybe_address.txt"
LIMIT = 30000

def new_list(limit=LIMIT):
    return [" ".join(producer.address().split("\n")).strip() for i in range(0, limit)]

maybe_addresses = get_lines(FILENAME, new_list)

def get_list(limit=LIMIT):
    if limit > LIMIT:
        raise "LIMIT is too high"
    if limit == LIMIT:
        return maybe_addresses
    return random.sample(maybe_addresses, limit)

def get_categorized(limit=LIMIT):
    return tag_category(MAYBE_ADDRESS, get_list(limit=limit))

def get_pipe():
    return generate_pipe(get_categorized())
