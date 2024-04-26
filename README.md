# GROUP-"I like studying" - lab 2 - variant 6

This is my lab2 of CPO class, implementation of immutable data structure dictionary
based on binary search tree(Variant6).

## Project structure

- `BinaryTreeDict.py` -- implementation of `TreeNode` class
                          and feature functions in `Features`.
- `BinaryTreeDict_test.py` -- unit and PBT test for `BinaryTreeDict`.

## Features

- Add element: `cons(key, value, node)`
- Remove element: `remove(key,node)`
- Size: `size(node)`
- Is member(getting value by key): `member(key, node)`
- From built-in dict: `from_dict(dictionary)`
- To built-in dict: `to_dict(node)`
- Filter dictionary: `mfilter(node, f)`
- Map dictionary: `mmap(node, f)`
- Reduce process elements: `reduce(n, f, state)`
- Iterator dictionary: `iterator(node)`
- Empty implementation: `mempty()`
- Concat implementation: `concat(dict1, dict2)`

## Contribution

- AnYifei (645192770@qq.com) -- all work.

## Changelog

- 26.4.2024 - 3
   - Update README.
   - Add code formatter to CI.
- 26.4.2024 - 2
   - Add unit tests .
   - Add PBT tests.
   - Implementation of part features
- 25.4.2024 - 0
   - Initialization.
   - Implementation of part features.

## Design notes

- Although the immutable implementation of lab2 is written from scratch,
  it still takes some ideas from immutable implementation, the basic
  ideas of BST data structure and function realization.
- In my opinion, data can be frequently modified, saving memory in mutable
  implementations, and it's simpler and more common than immutable
  implementations.
  In contrast, immutable implementation are suitable for thread safety,
  functional programming, and version control needs.
- Same as lab1 mutable implementation, the key will converted to type str
  when they are compared. The key is not allowed to be None in lab1, but in
  lab2 it is allowed to introduce a None value to key. Keys are still
  converted to str `str(key)` when compared even the key is None. I think
  this is an error in the implementation, but it still passes the tests.
  I considered using the hash of the key for comparison, but didn't implement
  it (because the tests passed).
