#!/usr/bin/env python3

import unittest


class Test1(unittest.TestCase):
    def test1(self):
        import termdoc

        lc = termdoc.LemmaCounts()
        lc.load("test_data/test1.tsv")

        self.assertEqual(lc.get_counts()["foo"], 10)
        self.assertEqual(lc.get_counts()["bar"], 5)
        self.assertEqual(lc.get_counts()["baz"], 5)
        self.assertEqual(lc.get_counts(("1",))["foo"], 9)
        self.assertEqual(lc.get_counts(("1",))["bar"], 5)
        self.assertEqual(lc.get_counts(("1",))["baz"], 0)
        self.assertEqual(lc.get_counts(("2",))["foo"], 1)
        self.assertEqual(lc.get_counts(("2",))["bar"], 0)
        self.assertEqual(lc.get_counts(("2",))["baz"], 5)
        self.assertEqual(lc.get_counts(("1", "1"))["foo"], 7)
        self.assertEqual(lc.get_counts(("1", "1"))["bar"], 4)
        self.assertEqual(lc.get_counts(("1", "1"))["baz"], 0)
        self.assertEqual(lc.get_counts(("1", "2"))["foo"], 2)
        self.assertEqual(lc.get_counts(("1", "2"))["bar"], 0)
        self.assertEqual(lc.get_counts(("1", "2"))["baz"], 0)
        self.assertEqual(lc.get_counts(("1", "3"))["foo"], 0)
        self.assertEqual(lc.get_counts(("1", "3"))["bar"], 1)
        self.assertEqual(lc.get_counts(("1", "3"))["baz"], 0)
        self.assertEqual(lc.get_counts(("2", "1"))["foo"], 1)
        self.assertEqual(lc.get_counts(("2", "1"))["bar"], 0)
        self.assertEqual(lc.get_counts(("2", "1"))["baz"], 5)


if __name__ == "__main__":
    unittest.main()
