import collections
from enum import Enum, auto


class Duplicates(Enum):
    ALLOW = auto()
    IGNORE = auto()
    ERROR = auto()


class HTDM:
    def __init__(self, duplicates=Duplicates.ALLOW):
        self.counters = []
        self.duplicates = duplicates

    def get_or_create_counter(self, depth):
        while depth > len(self.counters) - 1:
            self.counters.append(collections.defaultdict(collections.Counter))
        return self.counters[depth]

    def increment_count(self, address, term, count):
        first = True
        while True:
            depth = len(address)
            counter = self.get_or_create_counter(depth)[address]
            if first and term in counter:
                if self.duplicates == Duplicates.IGNORE:
                    return
                elif self.duplicates == Duplicates.ERROR:
                    raise ValueError(f"{term} already in {address}")
            counter[term] += count
            if depth == 0:
                break
            address = address[:-1]
            first = False

    def load(self, filename, field_sep="\t", address_sep="."):
        with open(filename) as f:
            for line in f:
                address_string, term, count_string = line.strip().split(field_sep)
                address = tuple(address_string.split(address_sep))
                count = int(count_string)
                self.increment_count(address, term, count)

    def get_counts(self, prefix=()):
        depth = len(prefix)
        return self.counters[depth][prefix]

    def prune(self, level):
        self.counters = self.counters[:level]

    def leaves(self):
        return self.counters[-1]

    def leaf_entries(self):
        for document, counter in self.leaves().items():
            for term, count in counter.items():
                yield document, term, count

    def graft(self, prefix, subtree):
        for address, term, count in subtree.leaf_entries():
            self.increment_count(prefix + address, term, count)
