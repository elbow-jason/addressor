from piper.utils import read_lines, tag_category
from piper.categories import NOTHING

import random

short_stories = read_lines("./data/short_stories.txt")
MAX_COUNT = len(short_stories)

def get_list(limit=MAX_COUNT):
    if limit > MAX_COUNT:
        raise Exception("MAX_COUNT too high")
    if limit is MAX_COUNT:
        return short_stories
    return random.sample(short_stories, limit)

def get_categorized(limit=MAX_COUNT):
    return tag_category(NOTHING, get_list(limit=limit))

