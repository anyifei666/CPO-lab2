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

- Since my dictionary data struction mutable implementation is based on
  binary search tree, so this is an ordered dictionary. The keys of the
  dictionary correspond to the indices of the binary search tree. Keys
  are unique and can be integers, floating-point values, or strings.
  During the binary search tree traversal, the keys are converted to
  string values. The order of the elements in the dictionary is only
  related to the key and is fixed. When the items are added to the dictionary,
  they are automatically sorted by their key and added to the binary search
  tree. So the order of the items in the dictionary can't be changed.
  I think this is a feature of the implementation, and probably a restriction
- In my opinion, unit tests are easy to understand and write, and the
  execution time is fast. Relatively speaking, PBT is more complex and takes
  longer to execute. Unit tests can only test a single function or module in
  the code, can't cover the behavior of the entire system. And unit tests may
  miss some edge cases or exceptions. In contrast, PBT describes the system
  behavior based on attributes, and can generate a large number of random test
  cases, which can cover more code paths and boundary cases. In addition,
  PBT can automatically generate test cases, reducing the workload of manually
  writing test cases.
