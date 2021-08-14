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

The core data structure is a term-document matrix supporting hierarchical documents. Documents are labelled with a delimited string such as "1.7.5" or "Plato.Republic.5". This hierarchy could represent divisions of a work, grouping of multiple works, or some combination. Counts are aggregated at each level of the hierarchy (including at the top level to get totals across all documents).

HTDMs can be loaded with `load`:

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

with a period-separated hierarchical address / document ID, term, and count all separated with tabs.

Both the period and tab are just defaults and can be override by passing `address_sep` and/or `field_sep` to `load`.

The HTDM can then give counts at any level of the document hierarchy:

```python
>>> c.get_counts()["foo"]
10
>>> c.get_counts("1")["foo"]
9
>>> c.get_counts("1.2")["foo"]
2

```

Note the separator used in the address / document ID defaults to a period (regardless of what was used in `load`) but can be override by passing `address_sep` to the HTDM constructor.

HTDMs can also be built up programmatically.

Here is an example with a single-level of documents (a traditional TDM):

```python
>>> import termdoc
>>> c = termdoc.HTDM()
>>> c.increment_count("1", "foo", 3)  # document 1 contains the term "foo" 3 times
>>> c.increment_count("1", "bar", 2)
>>> c.increment_count("2", "foo", 2)
>>> c.increment_count("2", "bar", 1)
>>> c.get_counts()["foo"]
5
>>> c.get_counts()["bar"]
3

```

And here is an example with a two-level hierarchy:

```python
>>> import termdoc
>>> c = termdoc.HTDM()
>>> c.increment_count("1.1", "foo", 3)
>>> c.increment_count("1.2", "foo", 3)
>>> c.increment_count("1.1", "bar", 2)
>>> c.increment_count("1.2", "bar", 2)
>>> c.increment_count("2.1", "foo", 2)
>>> c.increment_count("2.2", "foo", 2)
>>> c.increment_count("2.1", "bar", 1)
>>> c.increment_count("2.2", "bar", 1)
>>> c.get_counts()["foo"]
10
>>> c.get_counts()["bar"]
6
>>> c.get_counts("2")["foo"]
4

```

You can **prune** a HTDM to just `n` levels with the method `prune(n)`.

You can iterate over the document-term counts at the leaves of the HTDM with the method `leaf_entries()` (this returns a generator yielding `(document_address, term, count)` tuples). This is effectively a traditional TDM (the document IDs will still reflect the hierarchy but the aggregate counts aren't present).

You can optionally pass a `prefix` to `leaf_entries()` in each case only that subtree will be returns (with the prefix removed from the document IDs).

You can **graft** one HTDM under another by using the `graft(prefix, subtree)` method, specifying as `prefix` the document address you want to add the subtree under. This is useful if you have an HTDM for, say, a single work by an author, with chapters as documents and you want to incorporate that into a higher-level HTDM of multiple works by the author, or a collection of works by different authors.

Alternatively you can provide a `prefix` to `load` to load the file under a particular point in the tree. This effectively prepends the given `prefix` (plus address separator) to the document IDs.

The third (count) field in a loaded file can be omitted if the count is 1 and a document ID + term may be repeated with the counts accumulating.

You can deep copy an HTDM with `copy()`. You can also pass a prefix to `copy()` if you want to clone just a subtree.

You can save out an HTDM with `save()` which takes a `filename` and optional `field_sep` (defaulting to tab) and `prefix` (if you just want to save out a subtree).

### Duplicates Policy

You can optionally pass in a `duplicates` setting to the constructorr indicating the policy you want to follow if a term-document count is updated more than once.

```python
>>> c = termdoc.HTDM()
>>> c.increment_count("", "foo", 3)
>>> c.increment_count("", "foo", 2)
>>> c.get_counts()["foo"]
5

```

is the same as

```python
>>> c = termdoc.HTDM(duplicates=termdoc.Duplicates.ALLOW)
>>> c.increment_count("", "foo", 3)
>>> c.increment_count("", "foo", 2)
>>> c.get_counts()["foo"]
5

```

But you can tell an HTDM to ignore attempts to update an existing count:

```python
>>> c = termdoc.HTDM(duplicates=termdoc.Duplicates.IGNORE)
>>> c.increment_count("", "foo", 3)
>>> c.increment_count("", "foo", 2)
>>> c.get_counts()["foo"]
3

```

or to raise an exception:

```python
>>> c = termdoc.HTDM(duplicates=termdoc.Duplicates.ERROR)
>>> c.increment_count("", "foo", 3)
>>> c.increment_count("", "foo", 2)  # this will raise a ValueError
Traceback (most recent call last):
ValueError: 'foo' already in ''

```

Note that duplicates are only checked in the leaves of the document tree.

