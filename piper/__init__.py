
# Classification
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# Addresses
# https://www.randomlists.com/random-addresses


from piper import (
    parcel_number,
    mail_to,
    strict_address,
    escrow_number,
)

parcel_pipe = parcel_number.generate_pipe()
strict_address_pipe = strict_address.pipe

def run_text(text):
    text = preprocessing.clean(text)
    lines = preprocessing.to_lines(text)
    word_tokens = preprocessing.word_tokenize(text)
    sections = preprocessing.into_sections(text)
    sections = preprocessing.remove_empties(sections)
    section_tokens = [preprocessing.word_tokenize(s) for s in sections]
    return {
        "text": text,
        "word_tokens": word_tokens,
        "sections": sections,
        "section_tokens": section_tokens,
        "parcels": run_parcels(sections),
        "mail_to": run_mail_to(lines),
        "strict_address": run_strict_address(sections),
        "escrow_number": run_escrow_number(lines),
    }

def run_parcels(sections):
    predicted = parcel_pipe.predict(sections)
    labeled = list(zip(sections, predicted))
    found = parcel_number.filter_categorized(labeled)
    return parcel_number.extract(found)

def run_mail_to(lines, size=5):
    found = mail_to.find_lines(lines, size=size)
    extracted = [mail_to.extract(f) for f in found]
    return extracted

def run_strict_address(sections):
    predicted = strict_address.pipe.predict(sections)
    addrs = []
    for i in range(len(sections)):
        item = predicted[i]
        if item != 0:
            addrs.append(sections[i])
    addrs = [strict_address.extract(addr) for addr in addrs]
    return [addr for addr in addrs if len(addr) > 0]

def run_escrow_number(lines):
    return escrow_number.extract_lines(lines)
