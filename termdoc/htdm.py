import collections
from enum import Enum, auto


class Duplicates(Enum):
    ALLOW = auto()
    IGNORE = auto()
    ERROR = auto()


class HTDM:
    def __init__(self, address_sep=".", duplicates=Duplicates.ALLOW):
        self.counters = []
        self.address_sep = address_sep
        self.duplicates = duplicates

    def depth(self, address):
        if address:
            depth = len(address.split(self.address_sep))
        else:
            depth = 0
        return depth

    def get_or_create_counter(self, depth):
        while depth > len(self.counters) - 1:
            self.counters.append(collections.defaultdict(collections.Counter))
        return self.counters[depth]

    def increment_count(self, address, term, count):
        first = True
        while True:
            depth = self.depth(address)
            counter = self.get_or_create_counter(depth)[address]
            if first and term in counter:
                if self.duplicates == Duplicates.IGNORE:
                    return
                elif self.duplicates == Duplicates.ERROR:
                    raise ValueError(f"'{term}' already in '{address}'")
            counter[term] += count
            if depth == 0:
                break
            address = self.address_sep.join(address.split(self.address_sep)[:-1])
            first = False

    def load(self, filename, field_sep="\t", address_sep=None, prefix=None):
        address_sep = address_sep or self.address_sep
        with open(filename) as f:
            for line in f:
                fields = line.strip().split(field_sep)
                if len(fields) == 3:
                    address, term, count_string = fields
                    count = int(count_string)
                elif len(fields) == 2:
                    address, term = fields
                    count = 1
                else:
                    raise ValueError(f"{fields} should have 2 or 3 fields")
                if prefix:
                    address = prefix + address_sep + address
                self.increment_count(address, term, count)

    def save(self, filename, field_sep="\t", prefix=None):
        with open(filename, "w") as f:
            for document, term, count in self.leaf_entries(prefix):
                print(document, term, count, sep=field_sep, file=f)

    def get_counts(self, prefix=""):
        depth = self.depth(prefix)
        return self.counters[depth][prefix]

    def prune(self, level):
        self.counters = self.counters[:level]

    def leaves(self):
        return self.counters[-1]

    def leaf_entries(self, prefix=None):
        for document, counter in self.leaves().items():
            if prefix is None or document.startswith(prefix + self.address_sep):
                for term, count in counter.items():
                    if prefix:
                        subtree_document = document[len(prefix + self.address_sep) :]
                    else:
                        subtree_document = document
                    yield subtree_document, term, count

    def graft(self, prefix, subtree):
        for address, term, count in subtree.leaf_entries():
            self.increment_count(prefix + self.address_sep + address, term, count)

    def copy(self, prefix=None):
        new = HTDM(address_sep=self.address_sep, duplicates=self.duplicates)
        for document, term, count in self.leaf_entries(prefix):
            new.increment_count(document, term, count)
        return new
