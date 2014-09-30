import sys
import unittest

import undecorate


class TestUpdateWrapper(unittest.TestCase):

    def check_wrapper(self, wrapper, wrapped,
                      assigned=undecorate.WRAPPER_ASSIGNMENTS,
                      updated=undecorate.WRAPPER_UPDATES):
        # Check attributes were assigned
        for name in assigned:
            self.assertTrue(getattr(wrapper, name) is getattr(wrapped, name))
        # Check attributes were updated
        for name in updated:
            wrapper_attr = getattr(wrapper, name)
            wrapped_attr = getattr(wrapped, name)
            for key in wrapped_attr:
                if name == "__dict__" and key == "__wrapped__":
                    # __wrapped__ is overwritten by the update code
                    continue
                self.assertTrue(wrapped_attr[key] is wrapper_attr[key])
        # Check __wrapped__
        self.assertTrue(wrapper.__wrapped__ is wrapped)


    def _default_update(self):
        def f():
            """This is a test"""
            pass
        f.attr = 'This is also a test'
        f.__wrapped__ = "This is a bald faced lie"
        def wrapper():
            pass
        undecorate.update_wrapper(wrapper, f)
        return wrapper, f

    def test_default_update(self):
        wrapper, f = self._default_update()
        self.check_wrapper(wrapper, f)
        self.assertTrue(wrapper.__wrapped__ is f)
        self.assertEqual(wrapper.__name__, 'f')
        self.assertEqual(wrapper.attr, 'This is also a test')

    def test_no_update(self):
        def f():
            """This is a test"""
            pass
        f.attr = 'This is also a test'
        def wrapper():
            pass
        undecorate.update_wrapper(wrapper, f, (), ())
        self.check_wrapper(wrapper, f, (), ())
        self.assertEqual(wrapper.__name__, 'wrapper')
        self.assertEqual(wrapper.__doc__, None)
        self.assertFalse(hasattr(wrapper, 'attr'))

    def test_selective_update(self):
        def f():
            pass
        f.attr = 'This is a different test'
        f.dict_attr = dict(a=1, b=2, c=3)
        def wrapper():
            pass
        wrapper.dict_attr = {}
        assign = ('attr',)
        update = ('dict_attr',)
        undecorate.update_wrapper(wrapper, f, assign, update)
        self.check_wrapper(wrapper, f, assign, update)
        self.assertEqual(wrapper.__name__, 'wrapper')
        self.assertEqual(wrapper.__doc__, None)
        self.assertEqual(wrapper.attr, 'This is a different test')
        self.assertEqual(wrapper.dict_attr, f.dict_attr)

    def test_builtin_update(self):
        # Test for bug #1576241
        def wrapper():
            pass
        undecorate.update_wrapper(wrapper, max)
        self.assertEqual(wrapper.__name__, 'max')
        self.assertTrue(wrapper.__doc__.startswith('max('))

class TestWraps(TestUpdateWrapper):

    def _default_update(self):
        def f():
            """This is a test"""
            pass
        f.attr = 'This is also a test'
        f.__wrapped__ = "This is still a bald faced lie"
        @undecorate.wraps(f)
        def wrapper():
            pass
        return wrapper, f

    def test_default_update(self):
        wrapper, f = self._default_update()
        self.check_wrapper(wrapper, f)
        self.assertEqual(wrapper.__name__, 'f')
        self.assertEqual(wrapper.attr, 'This is also a test')

    def test_default_update_doc(self):
        wrapper, _ = self._default_update()
        self.assertEqual(wrapper.__doc__, 'This is a test')

    def test_no_update(self):
        def f():
            """This is a test"""
            pass
        f.attr = 'This is also a test'
        @undecorate.wraps(f, (), ())
        def wrapper():
            pass
        self.check_wrapper(wrapper, f, (), ())
        self.assertEqual(wrapper.__name__, 'wrapper')
        self.assertEqual(wrapper.__doc__, None)
        self.assertFalse(hasattr(wrapper, 'attr'))

    def test_selective_update(self):
        def f():
            pass
        f.attr = 'This is a different test'
        f.dict_attr = dict(a=1, b=2, c=3)
        def add_dict_attr(f):
            f.dict_attr = {}
            return f
        assign = ('attr',)
        update = ('dict_attr',)
        @undecorate.wraps(f, assign, update)
        @add_dict_attr
        def wrapper():
            pass
        self.check_wrapper(wrapper, f, assign, update)
        self.assertEqual(wrapper.__name__, 'wrapper')
        self.assertEqual(wrapper.__doc__, None)
        self.assertEqual(wrapper.attr, 'This is a different test')
        self.assertEqual(wrapper.dict_attr, f.dict_attr)
