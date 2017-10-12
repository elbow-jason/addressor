
from piper import escrow_number

WITH_RECORDERS = "Escrow No AZ5490 SPACE ABOVE THIS LINE FOR RECORDERS USE"

def test_escrow_number_extract_works():
    assert escrow_number.extract(WITH_RECORDERS) == "AZ5490"
