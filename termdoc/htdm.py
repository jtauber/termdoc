import collections
from dataclasses import dataclass
from enum import Enum, auto


class Duplicates(Enum):
    ALLOW = auto()
    IGNORE = auto()
    ERROR = auto()


@dataclass
class Address:
    as_string: str
    as_tuple: tuple


class DelimitedAddressFormatter:
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def __call__(self, address=()):
        if isinstance(address, str):
            return Address(
                as_string=address, as_tuple=tuple(address.split(self.delimiter))
            )
        elif isinstance(address, tuple):
            return Address(
                as_string=self.delimiter.join(map(str, address)),
                as_tuple=tuple(map(str, address)),
            )
        else:
            raise ValueError


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
        if isinstance(address, Address):
            address = address.as_tuple
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
                fields = line.strip().split(field_sep)
                if len(fields) == 3:
                    address_string, term, count_string = fields
                    count = int(count_string)
                elif len(fields) == 2:
                    address_string, term = fields
                    count = 1
                else:
                    raise ValueError(f"{fields} should have 2 or 3 fields")
                address = tuple(address_string.split(address_sep))
                self.increment_count(address, term, count)

    def get_counts(self, prefix=()):
        if isinstance(prefix, Address):
            prefix = prefix.as_tuple
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
        if isinstance(prefix, Address):
            prefix = prefix.as_tuple
        for address, term, count in subtree.leaf_entries():
            self.increment_count(prefix + address, term, count)
