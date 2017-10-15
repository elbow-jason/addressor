
# Classification
# http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

# Addresses
# https://www.randomlists.com/random-addresses


from piper import (
    parcel_number,
    mail_to,
    strict_address,
    escrow_number,
    organization,
    legal_person,
    first_name,
    last_name,
)

# parcel_pipe = parcel_number.generate_pipe()
# strict_address_pipe = strict_address.pipe
# organization_pipe = organization.pipe
# legal_person_pipe = legal_person.pipe

class TextDocument(object):
    def __init__(self, text):
        text = preprocessing.clean(text)
        self.text = text
        self.word_tokens = preprocessing.word_tokenize(text)
        self.lines = preprocessing.to_lines(text)
        self.parcel = []
        self.mail_to = []
        self.strict_address = []
        self.escrow_number = []
        self.organization = []
        self.legal_person = []
        self.first_name_exact = []
        self.first_name_fuzzy = []
        self.last_name_exact = []
        self.last_name_fuzzy = []
    
    @property
    def trigrams(self):
        return preprocessing.to_word_chunks(self.text, size=3)
    
    def chunks(self, size=15):
        return preprocessing.to_word_chunks(self.text, size=size)
    
    @property
    def sections(self):
        sections = preprocessing.into_sections(self.text)
        sections = preprocessing.remove_empties(sections)
        return sections

    @property
    def section_tokens(self):
        return [preprocessing.word_tokenize(s) for s in self.sections]

    def run(self):
        self.run_parcel()
        self.run_mail_to()
        self.run_strict_address(size=15)
        self.run_escrow_number()
        self.run_organization()
        self.run_legal_person(size=10)
        self.run_first_name_exact()
        self.run_first_name_fuzzy()
        self.run_last_name_exact()
        self.run_last_name_fuzzy()
        self.run_full_name()

    def run_parcel(self):
        self.parcel = parcel_number.extract(self.lines)
    
    def run_mail_to(self, size=5):
        found = mail_to.find_lines(self.lines, size=size)
        self.mail_to = [mail_to.extract(f) for f in found]

    def run_strict_address(self, size=15):
        chunks_15 = self.chunks(size=size)
        predicted = strict_address.pipe.predict(chunks_15)
        addrs = []
        for i in range(len(chunks_15)):
            item = predicted[i]
            if item != 0:
                addrs.append(chunks_15[i])
        addrs = [strict_address.extract(addr) for addr in addrs]
        addrs = [addr for addr in addrs if len(addr) > 0]
        self.strict_address = preprocessing.deduplicate_substrings(addrs)

    def run_escrow_number(self):
        self.escrow_number = escrow_number.extract_lines(self.lines)
    
    def run_organization(self):
        predicted = organization.pipe.predict(self.lines)
        labeled = list(zip(self.lines, predicted))
        found = organization.filter_categorized(labeled)
        self.organization = organization.extract(found)

    def run_legal_person(self, size=10):
        chunks = self.chunks(size=size)
        predicted = legal_person.pipe.predict(chunks)
        labeled = list(zip(chunks, predicted))
        found = legal_person.filter_categorized(labeled)
        self.legal_person = legal_person.extract(found)

    def run_first_name_fuzzy(self):
        found = first_name.extract(self.word_tokens)
        self.first_name_fuzzy = list(set(found))

    def run_first_name_exact(self):
        found = [t for t in self.word_tokens if t.lower() in first_name.names]
        self.first_name_exact = list(set(found))

    def run_last_name_fuzzy(self):
        self.last_name_fuzzy = list(set(last_name.extract(self.word_tokens)))

    def run_last_name_exact(self):
        found = [t for t in self.word_tokens if t.lower() in last_name.names]
        self.last_name_exact = list(set(found))


    def print_report(self):
        def print_it(field):
            print(field + "\n", getattr(self, field))

        print_it("parcel")
        print_it("mail_to")
        print_it("strict_address")
        print_it("escrow_number")
        print_it("organization")
        print_it("legal_person")
        print_it("first_name_exact")
        print_it("first_name_fuzzy")
        print_it("last_name_exact")
        print_it("last_name_fuzzy")
        print_it("text")

