#!/usr/bin/env python3

import os
import tempfile
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

    def test_load5(self):
        import termdoc

        c = termdoc.HTDM()
        c.load("test_data/test2.tsv", prefix="xxx")

        self.assertEqual(c.get_counts()["foo"], 10)
        self.assertEqual(c.get_counts()["bar"], 5)
        self.assertEqual(c.get_counts()["baz"], 5)
        self.assertEqual(c.get_counts("xxx")["foo"], 10)
        self.assertEqual(c.get_counts("xxx")["bar"], 5)
        self.assertEqual(c.get_counts("xxx")["baz"], 5)
        self.assertEqual(c.get_counts("xxx.1")["foo"], 9)
        self.assertEqual(c.get_counts("xxx.1")["bar"], 5)
        self.assertEqual(c.get_counts("xxx.1")["baz"], 0)
        self.assertEqual(c.get_counts("xxx.2")["foo"], 1)
        self.assertEqual(c.get_counts("xxx.2")["bar"], 0)
        self.assertEqual(c.get_counts("xxx.2")["baz"], 5)

    def test_save(self):
        import termdoc

        _, filename = tempfile.mkstemp()

        c1 = termdoc.HTDM()
        c1.load("test_data/test2.tsv")
        c1.save(filename)

        c2 = termdoc.HTDM()
        c2.load(filename)

        os.remove(filename)

        self.assertEqual(c2.get_counts()["foo"], 10)
        self.assertEqual(c2.get_counts()["bar"], 5)
        self.assertEqual(c2.get_counts()["baz"], 5)
        self.assertEqual(c2.get_counts("1")["foo"], 9)
        self.assertEqual(c2.get_counts("1")["bar"], 5)
        self.assertEqual(c2.get_counts("1")["baz"], 0)
        self.assertEqual(c2.get_counts("2")["foo"], 1)
        self.assertEqual(c2.get_counts("2")["bar"], 0)
        self.assertEqual(c2.get_counts("2")["baz"], 5)
        self.assertEqual(c2.get_counts("1.1")["foo"], 7)
        self.assertEqual(c2.get_counts("1.1")["bar"], 4)
        self.assertEqual(c2.get_counts("1.1")["baz"], 0)
        self.assertEqual(c2.get_counts("1.2")["foo"], 2)
        self.assertEqual(c2.get_counts("1.2")["bar"], 0)
        self.assertEqual(c2.get_counts("1.2")["baz"], 0)
        self.assertEqual(c2.get_counts("1.3")["foo"], 0)
        self.assertEqual(c2.get_counts("1.3")["bar"], 1)
        self.assertEqual(c2.get_counts("1.3")["baz"], 0)
        self.assertEqual(c2.get_counts("2.1")["foo"], 1)
        self.assertEqual(c2.get_counts("2.1")["bar"], 0)
        self.assertEqual(c2.get_counts("2.1")["baz"], 5)

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

    def test_leaf_entries_with_prefix(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1.1", "foo", 3)
        c.increment_count("1.1", "bar", 2)
        c.increment_count("1.2", "foo", 2)
        c.increment_count("1.2", "bar", 1)
        c.increment_count("2.1", "foo", 5)
        c.increment_count("2.1", "bar", 1)
        c.increment_count("2.2", "foo", 3)
        c.increment_count("2.2", "bar", 7)
        self.assertEqual(
            list(c.leaf_entries("1")),
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

    def test_copy1(self):
        import termdoc

        c1 = termdoc.HTDM()
        c1.increment_count("1.1", "foo", 3)
        c1.increment_count("1.1", "bar", 2)
        c1.increment_count("1.2", "foo", 2)
        c1.increment_count("1.2", "bar", 1)
        c1.increment_count("2.1", "foo", 5)
        c1.increment_count("2.1", "bar", 1)
        c1.increment_count("2.2", "foo", 3)
        c1.increment_count("2.2", "bar", 7)

        c2 = c1.copy()
        c2.increment_count("1.3", "foo", 2)
        self.assertEqual(c1.get_counts("1")["foo"], 5)
        self.assertEqual(c2.get_counts("1")["foo"], 7)

    def test_copy2(self):
        import termdoc

        c1 = termdoc.HTDM()
        c1.increment_count("1.1", "foo", 3)
        c1.increment_count("1.1", "bar", 2)
        c1.increment_count("1.2", "foo", 2)
        c1.increment_count("1.2", "bar", 1)
        c1.increment_count("2.1", "foo", 5)
        c1.increment_count("2.1", "bar", 1)
        c1.increment_count("2.2", "foo", 3)
        c1.increment_count("2.2", "bar", 7)

        c2 = c1.copy("1")
        self.assertEqual(c1.get_counts()["foo"], 13)
        self.assertEqual(c1.get_counts("1")["foo"], 5)
        self.assertEqual(c2.get_counts()["foo"], 5)


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


class Test3(unittest.TestCase):
    def test_two_arg_increment_count(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1", "foo")
        c.increment_count("1", "bar", 2)
        c.increment_count("2", "foo", 2)
        c.increment_count("2", "bar")
        self.assertEqual(c.get_counts()["foo"], 3)
        self.assertEqual(c.get_counts()["bar"], 3)

    def test_add(self):
        import termdoc

        c = termdoc.HTDM()
        c.add("1", ["foo", "bar", "bar", "baz"])
        c.add("2", ["foo", "foo", "bar"])
        self.assertEqual(c.get_counts()["foo"], 3)
        self.assertEqual(c.get_counts("2")["foo"], 2)
        self.assertEqual(c.get_counts("1")["bar"], 2)


class Test4(unittest.TestCase):
    def test_term_frequency(self):
        import termdoc

        c = termdoc.HTDM()
        c.increment_count("1", "foo")
        c.increment_count("1", "bar", 3)
        c.increment_count("2", "foo", 3)
        c.increment_count("2", "bar")
        self.assertEqual(c.tf("foo"), 0.5)
        self.assertEqual(c.tf("foo", "2"), 0.75)

    def test_document_frequency(self):
        import termdoc

        c = termdoc.HTDM()
        c.add("1.1", ["foo", "bar"])
        c.add("1.2", ["bar"])
        c.add("2.1", ["foo"])
        c.add("2.2", ["foo", "bar", "baz"])

        self.assertEqual(c.df("foo"), 0.75)
        self.assertEqual(c.df("bar"), 0.75)
        self.assertEqual(c.df("baz"), 0.25)
        self.assertEqual(c.df("foo", level=1), 1)
        self.assertEqual(c.df("bar", level=1), 1)
        self.assertEqual(c.df("baz", level=1), 0.5)
        self.assertEqual(c.df("foo", "1"), 0.5)
        self.assertEqual(c.df("bar", "1"), 1)
        self.assertEqual(c.df("baz", "1"), 0)
        self.assertEqual(c.df("foo", "2"), 1)
        self.assertEqual(c.df("bar", "2"), 0.5)
        self.assertEqual(c.df("baz", "2"), 0.5)
        self.assertEqual(c.df("foo", ""), 0.75)
        self.assertEqual(c.df("bar", ""), 0.75)
        self.assertEqual(c.df("baz", ""), 0.25)
        self.assertEqual(c.df("foo", "", level=1), 1)
        self.assertEqual(c.df("bar", "", level=1), 1)
        self.assertEqual(c.df("baz", "", level=1), 0.5)
        self.assertEqual(c.df("foo", level=2), 0.75)
        self.assertEqual(c.df("bar", level=2), 0.75)
        self.assertEqual(c.df("baz", level=2), 0.25)
        self.assertEqual(c.df("foo", "", level=2), 0.75)
        self.assertEqual(c.df("bar", "", level=2), 0.75)
        self.assertEqual(c.df("baz", "", level=2), 0.25)
        self.assertEqual(c.df("foo", "1", level=1), 0.5)
        self.assertEqual(c.df("bar", "1", level=1), 1)
        self.assertEqual(c.df("baz", "1", level=1), 0)
        self.assertEqual(c.df("foo", "2", level=1), 1)
        self.assertEqual(c.df("bar", "2", level=1), 0.5)
        self.assertEqual(c.df("baz", "2", level=1), 0.5)

    def test_simple_tf_idf(self):
        import termdoc

        c = termdoc.HTDM()
        c.add("1.1", ["foo", "bar"])
        c.add("1.2", ["bar"])
        c.add("2.1", ["foo"])
        c.add("2.2", ["foo", "bar", "baz"])

        self.assertEqual(c.tf_idf("foo", "1.1"), 0.062469368304149966)
        self.assertEqual(c.tf_idf("bar", "1.1"), 0.062469368304149966)
        self.assertEqual(c.tf_idf("baz", "1.1"), 0.0)

        self.assertEqual(c.tf_idf("foo", "1.2"), 0.0)
        self.assertEqual(c.tf_idf("bar", "1.2"), 0.12493873660829993)
        self.assertEqual(c.tf_idf("baz", "1.2"), 0.0)

        self.assertEqual(c.tf_idf("foo", "2.1"), 0.12493873660829993)
        self.assertEqual(c.tf_idf("bar", "2.1"), 0.0)
        self.assertEqual(c.tf_idf("baz", "2.1"), 0.0)

        self.assertEqual(c.tf_idf("foo", "2.2"), 0.041646245536099975)
        self.assertEqual(c.tf_idf("bar", "2.2"), 0.041646245536099975)
        self.assertEqual(c.tf_idf("baz", "2.2"), 0.20068666377598746)

        self.assertEqual(c.tf_idf("foo", "1"), 0.0)
        self.assertEqual(c.tf_idf("bar", "1"), 0.0)
        self.assertEqual(c.tf_idf("baz", "1"), 0.0)

        self.assertEqual(c.tf_idf("foo", "2"), 0.0)
        self.assertEqual(c.tf_idf("bar", "2"), 0.0)
        self.assertEqual(c.tf_idf("baz", "2"), 0.0752574989159953)

    def test_hierarchical_tf_idf(self):
        import termdoc

        c = termdoc.HTDM()
        c.add("1.1", ["foo", "bar"])
        c.add("1.2", ["bar"])
        c.add("2.1", ["foo"])
        c.add("2.2", ["foo", "bar", "baz"])

        self.assertEqual(c.tf_idf("foo", "1.1", "1"), 0.1505149978319906)
        self.assertEqual(c.tf_idf("bar", "1.1", "1"), 0.0)
        self.assertRaises(ZeroDivisionError, c.tf_idf, "baz", "1.1", "1")

        self.assertEqual(c.tf_idf("foo", "1.2", "1"), 0.0)
        self.assertEqual(c.tf_idf("bar", "1.2", "1"), 0.0)
        self.assertRaises(ZeroDivisionError, c.tf_idf, "baz", "1.2", "1")

        self.assertRaises(ValueError, c.tf_idf, "foo", "1.1", "2")

    def test_wikipedia(self):
        import termdoc

        c = termdoc.HTDM()
        c.add("1", ["this", "is", "a", "a", "sample"])
        c.add(
            "2", ["this", "is", "another", "another", "example", "example", "example"]
        )

        self.assertEqual(c.tf("this", "1"), 1 / 5)
        self.assertEqual(c.tf("this", "2"), 1 / 7)
        self.assertEqual(c.df("this"), 1)
        self.assertEqual(c.tf("example", "1"), 0)
        self.assertEqual(c.tf("example", "2"), 3 / 7)
        self.assertEqual(c.df("example"), 1 / 2)
        self.assertEqual(c.tf_idf("this", "1"), 0)
        self.assertEqual(c.tf_idf("this", "2"), 0)
        self.assertEqual(c.tf_idf("example", "1"), 0)
        self.assertEqual(c.tf_idf("example", "2"), 0.12901285528456335)


if __name__ == "__main__":
    unittest.main()
