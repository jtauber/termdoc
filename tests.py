#!/usr/bin/env python3

import unittest


class Test1(unittest.TestCase):
    def test_single_level(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1", "foo", 3)
        c.increment_count("1", "bar", 2)
        c.increment_count("2", "foo", 2)
        c.increment_count("2", "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)

    def test_multi_level(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1.1", "foo", 3)
        c.increment_count("1.2", "foo", 3)
        c.increment_count("1.1", "bar", 2)
        c.increment_count("1.2", "bar", 2)
        c.increment_count("2.1", "foo", 2)
        c.increment_count("2.2", "foo", 2)
        c.increment_count("2.1", "bar", 1)
        c.increment_count("2.2", "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 6)
        self.assertEqual(c.get_counts("2")["foo"], 4)

    def test_load1(self):
        import termdoc

        c = termdoc.HTDM()
        c.load("test_data/test1.tsv")

        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 5)
        self.assertEqual(c.get_counts()["baz"], 5)
        self.assertEqual(c.get_counts("1")["foo"], 9)
        self.assertEqual(c.get_counts("1")["bar"], 5)
        self.assertEqual(c.get_counts("1")["baz"], 0)
        self.assertEqual(c.get_counts("2")["foo"], 1)
        self.assertEqual(c.get_counts("2")["bar"], 0)
        self.assertEqual(c.get_counts("2")["baz"], 5)
        self.assertEqual(c.get_counts("1.1")["foo"], 7)
        self.assertEqual(c.get_counts("1.1")["bar"], 4)
        self.assertEqual(c.get_counts("1.1")["baz"], 0)
        self.assertEqual(c.get_counts("1.2")["foo"], 2)
        self.assertEqual(c.get_counts("1.2")["bar"], 0)
        self.assertEqual(c.get_counts("1.2")["baz"], 0)
        self.assertEqual(c.get_counts("1.3")["foo"], 0)
        self.assertEqual(c.get_counts("1.3")["bar"], 1)
        self.assertEqual(c.get_counts("1.3")["baz"], 0)
        self.assertEqual(c.get_counts("2.1")["foo"], 1)
        self.assertEqual(c.get_counts("2.1")["bar"], 0)
        self.assertEqual(c.get_counts("2.1")["baz"], 5)

    def test_load2(self):
        import termdoc

        c = termdoc.HTDM()
        c.load("test_data/test2.tsv")

        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 5)
        self.assertEqual(c.get_counts()["baz"], 5)
        self.assertEqual(c.get_counts("1")["foo"], 9)
        self.assertEqual(c.get_counts("1")["bar"], 5)
        self.assertEqual(c.get_counts("1")["baz"], 0)
        self.assertEqual(c.get_counts("2")["foo"], 1)
        self.assertEqual(c.get_counts("2")["bar"], 0)
        self.assertEqual(c.get_counts("2")["baz"], 5)
        self.assertEqual(c.get_counts("1.1")["foo"], 7)
        self.assertEqual(c.get_counts("1.1")["bar"], 4)
        self.assertEqual(c.get_counts("1.1")["baz"], 0)
        self.assertEqual(c.get_counts("1.2")["foo"], 2)
        self.assertEqual(c.get_counts("1.2")["bar"], 0)
        self.assertEqual(c.get_counts("1.2")["baz"], 0)
        self.assertEqual(c.get_counts("1.3")["foo"], 0)
        self.assertEqual(c.get_counts("1.3")["bar"], 1)
        self.assertEqual(c.get_counts("1.3")["baz"], 0)
        self.assertEqual(c.get_counts("2.1")["foo"], 1)
        self.assertEqual(c.get_counts("2.1")["bar"], 0)
        self.assertEqual(c.get_counts("2.1")["baz"], 5)

    def test_load3(self):
        import termdoc

        c = termdoc.HTDM()
        self.assertRaises(ValueError, c.load, "test_data/test3e.tsv")

    def test_load4(self):
        import termdoc

        c = termdoc.HTDM()
        self.assertRaises(ValueError, c.load, "test_data/test4e.tsv")

    def test_prune(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1", "foo", 3)
        c.increment_count("1", "bar", 2)
        c.increment_count("2", "foo", 2)
        c.increment_count("2", "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)
        self.assertEqual(len(c.counters), 2)
        c.prune(1)
        self.assertEqual(c.get_counts()["foo"], 5)
        self.assertEqual(c.get_counts()["bar"], 3)
        self.assertEqual(len(c.counters), 1)

    def test_leaf_entries(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1", "foo", 3)
        c.increment_count("1", "bar", 2)
        c.increment_count("2", "foo", 2)
        c.increment_count("2", "bar", 1)
        self.assertEqual(
            list(c.leaf_entries()),
            [
                ("1", "foo", 3),
                ("1", "bar", 2),
                ("2", "foo", 2),
                ("2", "bar", 1),
            ],
        )

    def test_graft(self):
        import termdoc

        c1 = termdoc.HTDM()
        c1.increment_count("1", "foo", 3)
        c1.increment_count("1", "bar", 2)
        c1.increment_count("2", "foo", 2)
        c1.increment_count("2", "bar", 1)
        c2 = termdoc.HTDM()
        c2.increment_count("4.1", "foo", 5)
        c2.increment_count("5.3", "foo", 6)
        c2.graft("5", c1)
        self.assertEqual(
            list(c2.leaf_entries()),
            [
                ("4.1", "foo", 5),
                ("5.3", "foo", 6),
                ("5.1", "foo", 3),
                ("5.1", "bar", 2),
                ("5.2", "foo", 2),
                ("5.2", "bar", 1),
            ],
        )


class TestDuplicates(unittest.TestCase):
    def test_allow(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("", "foo", 3)
        c.increment_count("", "foo", 2)
        self.assertEqual(c.get_counts()["foo"], 5)

    def test_explicit_allow(self):
        import termdoc

        c = termdoc.HTDM(duplicates=termdoc.Duplicates.ALLOW)
        c.increment_count("", "foo", 3)
        c.increment_count("", "foo", 2)
        self.assertEqual(c.get_counts()["foo"], 5)

    def test_ignore(self):
        import termdoc

        c = termdoc.HTDM(duplicates=termdoc.Duplicates.IGNORE)
        c.increment_count("", "foo", 3)
        c.increment_count("", "foo", 2)
        self.assertEqual(c.get_counts()["foo"], 3)

    def test_error(self):
        import termdoc

        c = termdoc.HTDM(duplicates=termdoc.Duplicates.ERROR)
        c.increment_count("", "foo", 3)
        self.assertRaises(ValueError, c.increment_count, "", "foo", 2)
        self.assertEqual(c.get_counts()["foo"], 3)

    def test_multi_level_error(self):
        import termdoc

        # this test makes sure the `if first` is working in `increment_count`
        c = termdoc.HTDM(duplicates=termdoc.Duplicates.ERROR)
        c.increment_count("1.1", "foo", 3)
        c.increment_count("1.2", "foo", 3)
        c.increment_count("1.1", "bar", 2)
        c.increment_count("1.2", "bar", 2)
        c.increment_count("2.1", "foo", 2)
        c.increment_count("2.2", "foo", 2)
        c.increment_count("2.1", "bar", 1)
        c.increment_count("2.2", "bar", 1)
        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 6)
        self.assertEqual(c.get_counts("2")["foo"], 4)


if __name__ == "__main__":
    unittest.main()
