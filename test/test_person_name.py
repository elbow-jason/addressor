
from piper import person_name

def test_full_name_correct_format():
    name = person_name.full_name()
    assert type(name) == str
    parts = name.split(" ")
    assert len(parts) == 3

def test_person_name_get_list():
    names = person_name.get_list(limit=25)
    assert len(names) == 25

