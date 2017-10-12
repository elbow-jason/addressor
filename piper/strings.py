import editdistance

def difference(a, b):
    avg_length = (len(a) + len(b)) / 2
    return distance(a, b) / avg_length

def similarity(a, b):
    return 1 - difference(a, b)

def distance(a, b):
    return editdistance.eval(a, b)
