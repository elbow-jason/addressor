from piper.parcel_number import generate_pipe, ParcelNumberPipe
from piper.parcel_number import APN_REGEX
from piper import parcel_number

from piper.categories import NOTHING, PARCEL_NUMBER

def test_generate_pipe():
    assert type(generate_pipe()) == ParcelNumberPipe

def test_predict_works():
    pipe = generate_pipe()
    result = pipe.predict(["Something something A.P.N.: 567-87-123"])
    assert result == [PARCEL_NUMBER]

def test_APN_REGEX_behaves_correctly():
    assert APN_REGEX.findall("a.p.n.: 567-87-123")[0] == "a.p.n.: 567-87-123"

def test_findall_works():
    phrase = "Something something A.P.N.: 567-87-123"
    assert parcel_number.findall(phrase) == ['a.p.n.: 567-87-123']

def test_extract_works():
    phrases = [
        "Something something A.P.N.: 567-87-123",
        "Other thingy that does not have our data",
        "another parcel no.: 333-33-333 and other things",
    ]
    pipe = generate_pipe()
    categorized = pipe.predict(phrases)
    assert categorized == [4, 0, 4]
    apn_lines = []
    for i in range(len(categorized)):
        if categorized[i] == PARCEL_NUMBER:
            apn_lines.append(phrases[i])
    extracted = parcel_number.extract(apn_lines)
    assert extracted == ['567-87-123', '333-33-333']

