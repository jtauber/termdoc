# termdoc

*Python library and tools for working with term-document matrices*

This project is just beginning, but a useful data structure, HTDM (hierarchical term-document matrix), is already available.

Various calculations on TDMs will soon be implemented, including TF-IDF.

I am also interested in standardizing the exchange format for HTDMs.

## Installation

```
pip install termdoc
```

## HTDM

The core data structure is a term-document matrix supporting hierarchical documents. Documents are labelled with a tuple such as `(1, 7, 5)` or `("Plato", "Republic", "Book 5")` (the type of each item in the tuple does not matter). Counts are aggregated at each level of the hierarchy (including at the top level to get totals across all documents).

Here is an example with a single-level of documents (a traditional TDM):

```python
>>> import termdoc
>>> c = termdoc.HTDM()
>>> c.increment_count((1,), "foo", 3)  # document 1 contains the term "foo" 3 times
>>> c.increment_count((1,), "bar", 2)
>>> c.increment_count((2,), "foo", 2)
>>> c.increment_count((2,), "bar", 1)
>>> c.get_counts()["foo"]
5
>>> c.get_counts()["bar"]
3
```

And here is an example with a two-level hierarchy:

```python
>>> import termdoc
>>> c = termdoc.HTDM()
>>> c.increment_count((1, 1), "foo", 3)
>>> c.increment_count((1, 2), "foo", 3)
>>> c.increment_count((1, 1), "bar", 2)
>>> c.increment_count((1, 2), "bar", 2)
>>> c.increment_count((2, 1), "foo", 2)
>>> c.increment_count((2, 2), "foo", 2)
>>> c.increment_count((2, 1), "bar", 1)
>>> c.increment_count((2, 2), "bar", 1)
>>> c.get_counts()["foo"]
10
>>> c.get_counts()["bar"]
6
>>> c.get_counts((2,))["foo"]
4
```

HTDMs can also be loaded with:

```python
>>> import termdoc
>>> c = termdoc.HTDM()
>>> c.load("test_data/test1.tsv")
```

where the file looks something like:

```
1.1	foo	7
1.1	bar	4
1.2	foo	2
1.3	bar	1
2.1	baz	5
2.1	foo	1
```

with a period-separated hierarchical document ID, term, and count all separated with tabs.

Both the period and tab are just defaults and can be override by padding `address_sep` and/or `field_sep` to `load`.

You can prune a HTDM to just `n` levels with the method `prune(n)`.
