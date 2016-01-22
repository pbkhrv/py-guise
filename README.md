# Work In Progress!

## Quick introduction

Guise is a lightweight Python library that allows you to easily verify that your value/object/iterable has a certain shape or structure, such as 'contains values of such type', 'has a particular key', 'is of length X' etc.

Let's say you are writing a function that accepts a list of points, like `[(12.5, 2), (98.14, 34.2), (42, 42)]`, and you want to make sure that it really only contains two-tuples of numbers. You would typically use a list comprehension for that:
```python
from numbers import Number

def is_list_of_points(pts):
    return all(isinstance(pt, tuple) and len(pt) == 2 and
               isinstance(pt[0], Number) and isinstance(pt[1], Number) for pt in pts)
```

Here is the same code, unpacked to make it more self-explanatory:
```python
def is_list_of_points(pts):
    is_number = lambda v: isinstance(v, Number)
    contains_only_numbers = lambda seq: all(is_number, seq)
    is_two_tuple = lambda tup: isinstance(tup, tuple) and len(tup) == 2
    return all(is_two_tuple(pt) and contains_only_numbers(pt) for pt in pts)
```

That's better, but still somewhat hard to understand what's happening at a glance. That's where Guise comes in. It lets you express your intent in a more declarative fashion:
```python
def is_list_of_points(pts):
    return guise.match([(Number, Number)], pts)
```

The "shape definition" `[(Number, Number)]` quite literally reads "a list of two-tuples that contain numbers".

Notice how that shape is the very first argument? That was done on purpose, so that fans of `functools` could easily use it with `partial`:
```python
from functools import partial

is_list_of_points = partial(guise.match, [(Number, Number)])

is_list_of_points([(12.5, 2), (98.14, 34.2), (42, 42)]) # => True
```

Actually, it's even easier than that: in order to save you some typing, guise.match() automatically returns a partial if you omit the second argument:
```python
is_list_of_points = guise.match([(Number, Number)])

is_list_of_points([(12.5, 2), (98.14, 34.2), (42, 42)]) # => True
is_list_of_points(['point', 'also point']) # => False
```

Let's look at another example. See if you can understand what it does before reading the explanation:
```python
import re
from guise import one_of

is_valid_polygon_object = guise.match({
    'points': [(Number, Number)],
    'stroke-style': one_of('dashed', 'dotted', 'solid'),
    'stroke-width': int,
    'stroke-color': re.compile('#[0-9a-f]{6}', flags=re.IGNORECASE)
})
```

Hopefully the intent is clear: it's a function that checks that a `dict` contains 4 keys. We expect the key 'points' to map to a list of X,Y coordinates (as seen before), 'stroke-style' - one of 3 possible strings, 'stroke-width' an int, and 'stroke-color' to map to an RGB color formatted to match the given regular expression.

One more example before we move on. This time we are verifying that a list or a tuple has an exact number of elements, and each element has a particular shape. This works great with `namedtuple`s:
```python
from collections import namedtuple

UserRecord = namedtuple('UserRecord', ['name', 'email', 'age', 'roles'])
user_template = UserRecord(name=str, email=re.compile('.+?\@.+'), age=int, roles=[str])

guise.match(user_template, ('Bob', 'bob@example.com', 26, ['admin', 'owner'])) # => True
```

## Ways to use the shape definitions

Guise allows you to apply a shape definition to objects in different ways:
- "exact match": the object must match the given definition *exactly*. The meaning of "exactly" depends on the shape. For instance, if we use the `dict` or `{}` shape, it means that the object in question must be a mapping and it must contain all of the specified keys and it must not contain keys that aren't included in the definition. Exact match can be performed on any object type, from None to primitive types to collections. All of the examples above are exact matches. See the `match()` function for more details.
- "contains": the object must be iterable and one or more of its elements must match the given shape. See the `contains()` function for more details.
- "partial match": the object must be iterable and it must contain elements that match all of the specified shapes, but, unlike in the case of exact match, it can also contain non-matching elements. It is equivalent to joining several `contains()` calls with boolean `and`, but without the boilerplate. See the `like()` function for more information.
- "recursive contains": the object must be iterable and must contain at least one element that either matches the shape or contains an element that matches the "recursive contains" definition. It allows you to search through a complex data structure for objects that match the given shape without having to write code to navigate the said structure.

## Ways to define shapes


## Convention over configuration


# Ideas and TODOs
- Add support for python 3.5 "typing" module
- explore 'with' as construct to validate guise likeness
- add field extraction from dicts to guise
- extract namedtuple from dict/tuple using guise
- Something sorta kinda similar in Clojure called seqex https://github.com/jclaggett/seqex
- voluptuous https://pypi.python.org/pypi/voluptuous/
- colander http://docs.pylonsproject.org/projects/colander/en/latest/
- https://pypi.python.org/pypi?%3Aaction=search&term=schema&submit=search
