#!/usr/bin/env python3

import unittest


class Test1(unittest.TestCase):
    def test1(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count((1,), "foo", 3)
        c.increment_count((1,), "bar", 2)
        c.increment_count((2,), "foo", 2)
        c.increment_count((2,), "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)

    def test2(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count((1, 1), "foo", 3)
        c.increment_count((1, 2), "foo", 3)
        c.increment_count((1, 1), "bar", 2)
        c.increment_count((1, 2), "bar", 2)
        c.increment_count((2, 1), "foo", 2)
        c.increment_count((2, 2), "foo", 2)
        c.increment_count((2, 1), "bar", 1)
        c.increment_count((2, 2), "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 6)
        self.assertEqual(c.get_counts((2,))["foo"], 4)

    def test3(self):
        import termdoc

        c = termdoc.HTDM()
        c.load("test_data/test1.tsv")

        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 5)
        self.assertEqual(c.get_counts()["baz"], 5)
        self.assertEqual(c.get_counts(("1",))["foo"], 9)
        self.assertEqual(c.get_counts(("1",))["bar"], 5)
        self.assertEqual(c.get_counts(("1",))["baz"], 0)
        self.assertEqual(c.get_counts(("2",))["foo"], 1)
        self.assertEqual(c.get_counts(("2",))["bar"], 0)
        self.assertEqual(c.get_counts(("2",))["baz"], 5)
        self.assertEqual(c.get_counts(("1", "1"))["foo"], 7)
        self.assertEqual(c.get_counts(("1", "1"))["bar"], 4)
        self.assertEqual(c.get_counts(("1", "1"))["baz"], 0)
        self.assertEqual(c.get_counts(("1", "2"))["foo"], 2)
        self.assertEqual(c.get_counts(("1", "2"))["bar"], 0)
        self.assertEqual(c.get_counts(("1", "2"))["baz"], 0)
        self.assertEqual(c.get_counts(("1", "3"))["foo"], 0)
        self.assertEqual(c.get_counts(("1", "3"))["bar"], 1)
        self.assertEqual(c.get_counts(("1", "3"))["baz"], 0)
        self.assertEqual(c.get_counts(("2", "1"))["foo"], 1)
        self.assertEqual(c.get_counts(("2", "1"))["bar"], 0)
        self.assertEqual(c.get_counts(("2", "1"))["baz"], 5)

    def test4(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count((1,), "foo", 3)
        c.increment_count((1,), "bar", 2)
        c.increment_count((2,), "foo", 2)
        c.increment_count((2,), "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)
        self.assertEqual(len(c.counters), 2)
        c.prune(1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)
        self.assertEqual(len(c.counters), 1)

    def test5(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count((1,), "foo", 3)
        c.increment_count((1,), "bar", 2)
        c.increment_count((2,), "foo", 2)
        c.increment_count((2,), "bar", 1)
        self.assertEqual(
            list(c.leaf_entries()), [
                ((1,), "foo", 3),
                ((1,), "bar", 2),
                ((2,), "foo", 2),
                ((2,), "bar", 1),
            ]
        )


if __name__ == "__main__":
    unittest.main()
