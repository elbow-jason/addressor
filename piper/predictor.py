from random import shuffle

from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import (CountVectorizer, TfidfTransformer)

from piper import nothing
from piper.categories import LABELS 

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

def generate_pipe(*categorized):
    nothings    = nothing.get_categorized()
    combined    = combine_and_shuffle(nothings, *categorized)
    data        = extract_data(combined)
    target      = extract_target(combined)
    vect        = CountVectorizer()
    tfidf       = TfidfTransformer()
    sgd_kwargs  = dict(loss='hinge', penalty='l2', alpha=1e-3, n_iter=12, random_state=49)
    clf         = SGDClassifier(**sgd_kwargs)
    pipe = Pipeline([
        ('vect', vect),
        ('tfidf', tfidf),
        ('clf', clf),
    ])
    pipe = pipe.fit(data, target)
    return pipe

def predict(pipe, items):
    predicted = pipe.predict(items)
    return [ LABELS[cat_index] for cat_index in predicted ]

def zip_dict(texts, labels):
    return dict(zip_list(texts, labels))

def zip_list(texts, labels):
    return list(zip(texts, labels))
