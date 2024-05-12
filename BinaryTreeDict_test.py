import itertools
import unittest
from hypothesis import given
import hypothesis.strategies as st
from typing import Dict, List
from BinaryTreeDict import cons, remove, size, member, to_dict, from_dict, \
    to_list, mmap, reduce, iterator, concat, mempty, mfilter


class TestBinaryTreeDict(unittest.TestCase):
    def test_cons(self) -> None:
        mydict = cons(42.5, 4,
                      cons(42, 3, cons('foo', 2, cons(None, 1, None))))
        self.assertEqual(str(mydict), "{42: 3, 42.5: 4, None: 1, 'foo': 2}")

    def test_api(self) -> None:
        empty = mempty()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons("a", 1, cons(None, "c", cons(2, "b", empty)))
        self.assertEqual(str(to_dict(empty)), "{}")
        self.assertTrue(
            str(l1) in [
                "{'a': 1, 2: 'b', None: 'c'}",
                "{'a': 1, None: 'c', 2: 'b'}",
                "{2: 'b', 'a': 1, None: 'c'}",
                "{2: 'b', None: 'c', 'a': 1}",
                "{None: 'c', 2: 'b', 'a': 1}",
                "{None: 'c', 'a': 1, 2: 'b'}"
            ]
        )

        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)

        self.assertEqual(size(empty), 0)
        self.assertEqual(size(l1), 3)
        self.assertEqual(size(l2), 3)

        self.assertTrue(str(remove(l1, None)) in [
            "{2: 'b', 'a': 1}",
            "{'a': 1, 2: 'b'}"
        ])

        self.assertTrue(str(remove(l1, 'a')) in [
            "{2: 'b', None: 'c'}",
            "{None: 'c', 2: 'b'}"
        ])

        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member('a', l1))
        self.assertTrue(member(2, l1))
        self.assertFalse(member(3, l1))

        self.assertIn(to_dict(l1),
                      map(dict, itertools.permutations
                      ([('a', 1), (2, 'b'), (None, 'c')])))

        self.assertEqual(l1, from_dict({'a': 1, 2: 'b', None: 'c'}))
        self.assertEqual(l1, from_dict({'a': 1, 2: 'b', None: 'c'}))

        self.assertEqual(concat(l1, l2),
                         from_dict({'a': 1, 2: 'b', None: 'c'}))

        buf = []
        for k, v in iterator(l1):
            buf.append(k)
        self.assertIn(buf, map(list, itertools.permutations(['a', 2, None])))

        lst = (list(map(lambda e: e[0], to_list(l1))) +
               list(map(lambda e: e[0], to_list(l2))))
        for k, v in iterator(l1):
            lst.remove(k)
        for k, v in iterator(l2):
            lst.remove(k)
        self.assertEqual(lst, [])

    def test_filter(self) -> None:
        mydict = from_dict({1: 1, 2: "a", "b": 3, "4": 4, 5: None})
        self.assertEqual(
            mfilter(mydict, lambda key, value: isinstance(key, int)),
            {1: 1, 2: "a", 5: None}
        )
        self.assertEqual(
            mfilter(mydict, lambda key, value: isinstance(value, int)),
            {1: 1, "4": 4, "b": 3}
        )

    def test_to_dict(self) -> None:
        pydict = to_dict(cons(3, "three",
                              cons(2, "two",
                                   cons(1, "one", None))))
        self.assertEqual(pydict[1], 'one')
        self.assertEqual(pydict[2], 'two')

    def test_from_dict(self) -> None:
        # 测试从Python字典构建
        pydict: Dict[int | str | float | None, int | str | float | None] = {
            '1': 'one', 2: 'two', 3: None}
        mydict = from_dict(pydict)
        self.assertEqual(size(mydict), 3)
        self.assertEqual(member('1', mydict), 'one')

    def test_empty(self) -> None:
        empty_dict = mempty()
        self.assertEqual(size(empty_dict), 0)

    def test_map(self) -> None:
        mydict = from_dict({1: 1, 2: 2, 3: 3, 4: 4, 5: 5})
        self.assertEqual(
            mmap(mydict, lambda key, value: (str(key), str(value))),
            {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5"},
        )

    def test_reduce(self) -> None:
        mydict = from_dict({})
        self.assertEqual(reduce(mydict,
                                lambda key, value, st:
                                st, 0), 0)
        test_data: List[
            Dict[int | str | float | None, int | str | float | None]] \
            = [{}, {"a": "1", "b": "2"}, {"a": "1", "b": "2", "c": "3"}]
        for e in test_data:
            mydict = from_dict(e)
            self.assertEqual(
                reduce(mydict, lambda key, value, st: st + 1, 0), size(mydict)
            )

    @given(
        st.dictionaries(st.text(), st.text()),
        st.dictionaries(st.text(), st.text()),
        st.dictionaries(st.text(), st.text()),
    )
    def test_PBT_monoid_Associativity(self,
                                      a: Dict[
                                          int | str | float | None,
                                          int | str | float | None],
                                      b: Dict[
                                          int | str | float | None,
                                          int | str | float | None],
                                      c: Dict[
                                          int | str | float | None,
                                          int | str | float | None]) -> None:
        dict_a = from_dict(a)
        dict_b = from_dict(b)
        dict_c = from_dict(c)
        dict1 = concat(dict_a, dict_b)
        dict2 = concat(dict_b, dict_c)
        self.assertEqual(concat(dict1, dict_c),
                         concat(dict_a, dict2))

    @given(st.dictionaries(st.text(), st.text()))
    def test_PBT_monoid_Identity_element(self,
                                         a: Dict[
                                             int | str | float | None,
                                             int | str | float | None]) \
            -> None:
        # test for Identity element (empty_dict)
        empty_dict = mempty()
        mydict = from_dict(a)
        self.assertEqual(concat(empty_dict, mydict), mydict)
        self.assertEqual(concat(mydict, empty_dict), mydict)
