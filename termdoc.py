import collections


class LemmaCounts:
    def __init__(self):
        self.counters = []

    def get_or_create_counter(self, depth):
        while depth > len(self.counters) - 1:
            self.counters.append(collections.defaultdict(collections.Counter))
        return self.counters[depth]

    def increment_count(self, address, lemma, count):
        while True:
            depth = len(address)
            self.get_or_create_counter(depth)[address][lemma] += count
            if depth == 0:
                break
            address = address[:-1]

    def load(self, filename):
        with open(filename) as f:
            for line in f:
                address_string, lemma, count_string = line.strip().split("\t")
                address = tuple(address_string.split("."))
                count = int(count_string)
                self.increment_count(address, lemma, count)

    def get_counts(self, prefix=()):
        depth = len(prefix)
        return self.counters[depth][prefix]
