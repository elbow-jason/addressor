
from piper.parcel_number import APN_REGEX
from piper import parcel_number

from piper.categories import NOTHING, PARCEL_NUMBER

def test_APN_REGEX_behaves_correctly():
    found = APN_REGEX.search("a.p.n.: 567-87-123")
    assert found.groupdict().get("key") == "567-87-123"

def test_extract_works():
    phrases = [
        "Something something A.P.N.: 567-87-123",
        "Other thingy that does not have our data",
        "another parcel no.: 333-33-333 and other things",
    ]
    extracted = parcel_number.extract(phrases)
    assert extracted == ['567-87-123', '333-33-333']

