import random
from faker import Faker

from piper.utils import (
    open_data_type,
    tag_category,
    get_lines,
)
from piper.categories import PERSON_NAME
from piper.predictor import generate_pipe

producer = Faker()

FILENAME = "./data/person_names.txt"
LIMIT = 30000

def middle_initial():
    return producer.random_letter().upper() + "."

def full_name():
    parts = producer.name().split(" ")
    return " ".join([parts[0], middle_initial(), parts[1]])

def new_list(limit=LIMIT):
    return [full_name() for i in range(0, limit)]

person_names = get_lines(FILENAME, new_list)

def get_list(limit=LIMIT):
    if limit > LIMIT:
        raise "LIMIT is too high"
    if limit == LIMIT:
        return person_names
    return random.sample(person_names, limit)

def get_categorized(limit=LIMIT):
    return tag_category(PERSON_NAME, get_list(limit=limit))

def get_pipe():
    return generate_pipe(get_categorized())
