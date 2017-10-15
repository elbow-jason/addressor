from piper.text_search import TextSearch

with open("./data/first_names.txt") as f:
    names = set(name.strip() for name in f.readlines())

index = TextSearch()
for name in names:
    index.add_word(name)

def search_names(token):
    return index.search(token.lower())

def is_titlized(token):
    return len(token) > 0 and token[0].isupper()

def fuzzy_matches(token):
    found = search_names(token)
    return [word for (word, _, similarity) in found if similarity >= 0.80]

def extract(tokens):
    kept = []
    for t in tokens:
        if not is_titlized(t):
            continue
        if not any(fuzzy_matches(t)):
            continue
        kept.append(t)
    return kept
