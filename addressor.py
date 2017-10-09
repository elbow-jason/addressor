
# Classification
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# Addresses
# https://www.randomlists.com/random-addresses


from random import shuffle

from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)

CATEGORIES = ["address", "nothing"]

def open_data_type(name, category):
    with open(name) as f:
        return [(category, line.strip()) for line in f.readlines()]

def get_short_stories():
    return open_data_type("short_stories.txt", 1)

def get_addresses():
    return open_data_type("addresses.txt", 0)

def combine_and_shuffle(*args):
    combined = []
    for item in args:
        combined = combined + item
    shuffle(combined) # shuffle mutates list in place
    return combined

def extract_data(items):
    return [dat for (_, dat) in items]

def extract_target(items):
    return [tar for (tar, _) in items]

def generate_pipe():
    addresses       = get_addresses()
    not_addresses   = get_short_stories()
    combined        = combine_and_shuffle(addresses, not_addresses)
    data            = extract_data(combined)
    target          = extract_target(combined)

    pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                              alpha=1e-3, n_iter=12, random_state=49)),
    ])
    pipe = pipe.fit(data, target)
    return pipe

def predict(pipe, items):
    predicted = pipe.predict(items)
    return [ CATEGORIES[cat] for cat in predicted ]
