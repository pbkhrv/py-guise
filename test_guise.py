import unittest
from numbers import Number
import guise as g

# Useful for:
# - unit testing
# - "contract testing" of APIs
# - declaring input/output value shapes
# - routing requests based on the shape of incoming data
#
# Features:
# - can be used with difflib to produce meaningful diff reports
# - is_seq_of(obj, shape) - check if obj is a sequence of objects that fit the given shape
#
#
#
#
#

#
# Primitive types
#
class TestGuiseTypes(unittest.TestCase):
    def test_none(self):
        self.assertTrue(g.fit(None, None))
        self.assertFalse(g.fit(None, 1))
        self.assertFalse(g.fit(None, False))
        self.assertFalse(g.fit(None, ''))
        self.assertFalse(g.fit(None, []))
        self.assertFalse(g.fit(None, {}))

    def test_str_type_fits_any_str(self):
        self.assertTrue(g.fit(str, ''))
        self.assertTrue(g.fit(str, 'asdf'))
        self.assertFalse(g.fit(str, 1))
        self.assertFalse(g.fit(str, True))
        self.assertFalse(g.fit(str, ['']))
        self.assertFalse(g.fit(str, {'asdf':''}))
        self.assertFalse(g.fit(str, None))

    def test_str_value_equality(self):
        self.assertTrue(g.fit('abc', 'abc'))
        self.assertFalse(g.fit('abc', 'ABC'))
        self.assertFalse(g.fit('abc', 1))
        self.assertFalse(g.fit('abc', True))
        self.assertFalse(g.fit('abc', ['abc']))
        self.assertFalse(g.fit('abc', {'abc':'abc'}))
        self.assertFalse(g.fit('abc', None))

    def test_int_type_fits_any_int(self):
        self.assertTrue(g.fit(int, 0))
        self.assertTrue(g.fit(int, 10))
        self.assertFalse(g.fit(int, False))
        self.assertFalse(g.fit(int, 0.0))
        self.assertFalse(g.fit(int, '0'))
        self.assertFalse(g.fit(int, [0]))
        self.assertFalse(g.fit(int, {}))
        self.assertFalse(g.fit(int, None))

    def test_float_type_fits_any_float(self):
        self.assertTrue(g.fit(float, 0.0))
        self.assertTrue(g.fit(float, 10.0))
        self.assertFalse(g.fit(float, False))
        self.assertFalse(g.fit(float, '0.0'))
        self.assertFalse(g.fit(float, [0.0]))
        self.assertFalse(g.fit(float, {}))
        self.assertFalse(g.fit(float, None))

    def test_number_type_fits_ints_and_floats(self):
        self.assertTrue(g.fit(Number, 0))
        self.assertTrue(g.fit(Number, 0.0))
        self.assertFalse(g.fit(Number, '0'))
        self.assertFalse(g.fit(Number, [0]))
        self.assertFalse(g.fit(Number, {}))
        self.assertFalse(g.fit(Number, False))
        self.assertFalse(g.fit(Number, None))

    def test_float_doesnt_fit_int(self):
        self.assertFalse(g.fit(float, 0))

    def test_int_doesnt_fit_float(self):
        self.assertFalse(g.fit(int, 1.0))

    def test_literal_number_equality(self):
        self.assertTrue(g.fit(123.0, 123.0))
        self.assertTrue(g.fit(123, 123))
        self.assertTrue(g.fit(123, 123.0))
        self.assertTrue(g.fit(123.0, 123))
        self.assertFalse(g.fit(123.0, False))
        self.assertFalse(g.fit(123.0, '123.0'))
        self.assertFalse(g.fit(123.0, [123.0]))
        self.assertFalse(g.fit(123.0, {}))
        self.assertFalse(g.fit(123.0, None))

    def test_bool_type_fits_any_bool(self):
        self.assertTrue(g.fit(bool, True))
        self.assertTrue(g.fit(bool, False))
        self.assertFalse(g.fit(bool, 0))
        self.assertFalse(g.fit(bool, 'True'))
        self.assertFalse(g.fit(bool, []))
        self.assertFalse(g.fit(bool, {}))
        self.assertFalse(g.fit(bool, None))

    def test_bool_value_equality(self):
        self.assertTrue(g.fit(True, True))
        self.assertTrue(g.fit(False, False))
        self.assertFalse(g.fit(True, 1))
        self.assertFalse(g.fit(True, 'True'))
        self.assertFalse(g.fit(True, [True]))
        self.assertFalse(g.fit(True, {}))
        self.assertFalse(g.fit(True, None))

#
# Lists
#
# "List" shape matches lists and tuples of arbitrary length.
# Each element of such lists and tuples must fit one of the given shapes, in any order.
#
class TestGuiseLists(unittest.TestCase):
    def test_list_type_fits_any_list(self):
        self.assertTrue(g.fit(list, []))
        self.assertTrue(g.fit(list, [1,2,3]))
        self.assertFalse(g.fit(list, {'a': 1}))
        self.assertFalse(g.fit(list, 1))
        self.assertFalse(g.fit(list, 'a'))
        self.assertFalse(g.fit(list, True))
        self.assertFalse(g.fit(list, None))

    def test_empty_list_means_no_values(self):
        self.assertTrue(g.fit([], []))
        self.assertTrue(g.fit([], ()))
        self.assertFalse(g.fit([], [1,2,3]))
        self.assertFalse(g.fit([], {}))
        self.assertFalse(g.fit([], 0))
        self.assertFalse(g.fit([], ''))
        self.assertFalse(g.fit([], False))
        self.assertFalse(g.fit([], None))

    def test_list_of_typed_values_cannot_be_empty(self):
        self.assertFalse(g.fit([str], []))
        self.assertFalse(g.fit([int], []))
        self.assertFalse(g.fit([float], []))
        self.assertFalse(g.fit([bool], []))
        self.assertFalse(g.fit([list], []))
        self.assertFalse(g.fit([dict], []))

    def test_list_of_strings(self):
        self.assertTrue(g.fit([str], ['asdf','erw']))
        self.assertTrue(g.fit([str], ('tup',)))
        self.assertFalse(g.fit([str], [1,2,3]))
        self.assertFalse(g.fit([str], [1,'2',3]))

    def test_list_of_ints(self):
        self.assertTrue(g.fit([int], [1]))
        self.assertTrue(g.fit([int], (1,2,3)))
        self.assertFalse(g.fit([int], [1,2.4,3]))
        self.assertFalse(g.fit([int], [True,1]))
        self.assertFalse(g.fit([int], [1,'2',3]))

    def test_list_of_floats(self):
        self.assertTrue(g.fit([float], [1.0,2.1,3.0]))
        self.assertFalse(g.fit([float], (1.0,2.1,3)))
        self.assertFalse(g.fit([float], [True,1.1]))
        self.assertFalse(g.fit([float], [1.0,'2.5',3]))

    def test_list_of_bools(self):
        self.assertTrue(g.fit([bool], [True, False]))
        self.assertFalse(g.fit([bool], [True, 0]))
        self.assertFalse(g.fit([bool], [True, 'False']))
        self.assertFalse(g.fit([bool], [True, []]))

    def test_list_of_lists(self):
        self.assertTrue(g.fit([list], [[1,2,3],['a','b','c']]))
        self.assertFalse(g.fit([list], ['a',['b','c']]))

    def test_list_of_dicts(self):
        self.assertTrue(g.fit([dict], [{}]))
        self.assertTrue(g.fit([dict], [{'a': 1}, {}]))
        self.assertFalse(g.fit([dict], [0, {}]))

    def test_list_of_mixed_types(self):
        self.assertTrue(g.fit([bool,list], [[], True, ['a','b']]))
        self.assertTrue(g.fit([int,dict], [1, {}, {}, 4]))
        self.assertTrue(g.fit([str,int], [1,'234']))
        self.assertFalse(g.fit([int,str], [True, 'False']))

    def test_list_of_mixed_any_order(self):
        self.assertTrue(g.fit([int,str], [1,'234',5]))
        self.assertTrue(g.fit([str,int], [1,'234',5]))

    def test_list_of_mixed_any_length(self):
        self.assertTrue(g.fit([int,str], [1,'234',5]))
        self.assertTrue(g.fit([int,str], [1,'234',5, 2]))
        self.assertTrue(g.fit([int,str], [1,'234',5, 2, 'more', 'zeroes']))

    def test_list_of_mixed_types(self):
        self.assertTrue(g.fit([1,2,3,bool], [3,1,True,1,False,2]))
        self.assertTrue(g.fit(['a','b'], ['a','b','b','b','a']))
        self.assertTrue(g.fit([[int],[str]], [['a','b'],[1,2]]))
        self.assertFalse(g.fit([1,2,3,bool], ['3',1,True,1,False,2]))
        self.assertFalse(g.fit([[int],[str]], [[1,'b'],['a',2]]))

#
# Tuple
#
# "Tuple" shape describes a list or a tuple of elements where each element fits each specified shape, in order.
# Order of elements is important.
# Length of the list is important.
# Useful for matching "records".
class TestGuiseTupleShape(unittest.TestCase):
    def test_empty_tuple_means_no_values(self):
        self.assertTrue(g.fit((), []))
        self.assertTrue(g.fit((), ()))
        self.assertFalse(g.fit((), [1]))
        self.assertFalse(g.fit((), ('')))
        self.assertFalse(g.fit((), ''))
        self.assertFalse(g.fit((), 0))
        self.assertFalse(g.fit((), {}))
        self.assertFalse(g.fit((), None))

    def test_tuple_single_type(self):
        self.assertTrue(g.fit((int,), [0]))
        self.assertTrue(g.fit((str,), ('a',)))
        self.assertFalse(g.fit((str,), (0,)))
        self.assertFalse(g.fit((int,), ['1']))

    def test_tuple(self):
        self.assertTrue(g.fit((int, int, int), [0, 1, 2]))
        self.assertTrue(g.fit((str, int, int), ('a', 1, 2)))
        self.assertTrue(g.fit((list, list), (['a'], [1, 2])))

    def test_tuple_important_order(self):
        self.assertFalse(g.fit((str, int, int), (0, '1', 2)))
        self.assertFalse(g.fit((bool, str, int), (0, 'abc', False)))

    def test_tuple_important_length(self):
        self.assertFalse(g.fit((int,), [0, 1]))
        self.assertFalse(g.fit((str, str), ['one string']))

    def test_tuple_concrete(self):
        self.assertTrue(g.fit(('Activate', int, dict), ['Activate', 1, {'go': 'forth'}]))
        self.assertTrue(g.fit((0, [int], dict), [0, [1,2,3], {'go': 'forth'}]))
        self.assertFalse(g.fit(('Activate', int, {}), [1, 'Activate', {'go': 'forth'}]))

#
# Dict
#
# "Dict" shape describes a dict with keys and values that fit given shapes
class TestGuiseDictShape(unittest.TestCase):
    def test_empty_dict_means_no_contents(self):
        self.assertTrue(g.fit({}, {}))
        self.assertFalse(g.fit({}, {'a': 'b'}))

    def test_dict_type_means_any_dict(self):
        self.assertTrue(g.fit(dict, {}))
        self.assertTrue(g.fit(dict, {1: 'one'}))

    def test_dict_concrete_keys_match_exactly(self):
        self.assertTrue(g.fit({'a': int, 'b': bool}, {'a': 1, 'b': True}))
        self.assertFalse(g.fit({'a': int, 'b': bool}, {'a': 1, 'b': True, 'c': []}))

    def test_dict_typed_keys_catch_all(self):
        self.assertTrue(g.fit({str: int}, {'a': 1, 'b': 2}))

    def test_dict_all_shapes_must_be_present(self):
        self.assertFalse(g.fit({'a': str, 'b': int}, {'a': 'str'}))

#
# Set
#
# "Set" shape is like an "or" operator that combines other shapes
class TestGuiseSetShape(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
