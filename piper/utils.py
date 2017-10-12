from os import path

def open_data_type(filename, category):
    with open(filename) as f:
        return [(category, line.strip()) for line in f.readlines()]

def tag_category(category, items):
    return [(category, item) for item in items]

def read_lines(filename):
     with open(filename) as f:
         return [x.strip() for x in f.readlines()]

def get_lines(filename, new_list_function):
    if path.isfile(filename):
        with open(filename, "r") as f:
            return [x.strip() for x in f.readlines()]
    else:
        lines = new_list_function()
        with open(filename, "w") as f:
            f.write("\n".join(lines))
        return [line.strip() for line in lines]

