"""Allow your decorations to be un-decorated.

In some cases, such as when testing, it can be useful to access the
decorated class or function directly, so as to not to use the behavior
or interface that the decorator might introduce.

Example:

>>> from functools import wraps
>>> from undecorate import unwrap, unwrappable
>>>
>>> @unwrappable
... def pack(func):
...     @wraps(func)
...     def wrapper(args, kwargs):
...         return func(*args, **kwargs)
...     return wrapper
...
>>> @pack
... def myfunc(a, b, c=None, d=None):
...     return (a, b, c, d)
...
>>> myfunc('a', 'b', c='c')
Traceback (most recent call last):
    ...
TypeError: wrapper() got an unexpected keyword argument 'c'
>>>
>>> unwrap(myfunc)('a', 'b', c='c')
('a', 'b', 'c', None)
"""

import functools


WRAPPER_ASSIGNMENTS = functools.WRAPPER_ASSIGNMENTS
WRAPPER_UPDATES = functools.WRAPPER_UPDATES


def update_wrapper(wrapper,
                   wrapped,
                   assigned=WRAPPER_ASSIGNMENTS,
                   updated=WRAPPER_UPDATES):
    """Backport setting __wrapped__ from functools.update_wrapper().

    Python 3.2 introduced, and Python 3.3 fixed, a new feature to
    functools.update_wrapper() that adds a __wrapped__ attribute to the
    wrapper function.

    This is a backport of that fixed functionality, built on top of
    functools.update_wrapper().
    """
    wrapper = functools.update_wrapper(
        wrapper, wrapped, assigned=assigned, updated=updated)
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped,
          assigned=WRAPPER_ASSIGNMENTS,
          updated=WRAPPER_UPDATES):
    """Decorator factory to apply backported update_wrapper()."""
    return functools.partial(update_wrapper, wrapped=wrapped,
                             assigned=assigned, updated=updated)


def unwrappable(decorator):
    """Make a decorator able to be un-decorated.

    This meta-decorator takes a decorator, and returns a new decorator
    that allows the wrapper to be used by unwrap().

    This is unneeded in Python 3.3+, where the __wrapped__ attribute
    is updated properly, if the wrapper is updated using functools.wraps or
    functools.update_wrapper. The __wrapped__ attribute that gets added in
    Python 3.2 always points to the innermost wrapped function.
    """
    @wraps(decorator)
    def meta_wrapper(wrapped):
        wrapper = decorator(wrapped)
        wrapper.__wrapped__ = wrapped
        return wrapper
    return meta_wrapper


def unwrap(wrapper):
    """Remove the wrapper, recursively all the way down."""
    while True:
        wrapped = getattr(wrapper, '__wrapped__', None)
        if wrapped is None:
            return wrapper
        wrapper = wrapped


CLASS_WRAPPER_ASSIGNMENTS = ('__module__', '__doc__')


def create_class_wrapper(wrapper,
                         wrapped,
                         assigned=CLASS_WRAPPER_ASSIGNMENTS):
    """Create a wrapper class that looks like the wrapped class.

    wrapper is the class used to override the wrapped class.
    wrapped is the class has values overridden by the wrapper.
    deleted is a tuple naming the __dict__ items to be removed from the
    wrapper class (defaults to CLASS_WRAPPER_DELETES).
    assigned is a tuple naming the __dict__ items to be copied directly
    from the wrapped class (defaults to CLASS_WRAPPER_ASSIGNMENTS).

    A notable difference from update_wrapper is that is creates a new class
    that does not appear to be exactly the same as the wrapped class, but
    rather mimics the name and the module, and inherits from the original
    class, relying on class inheritance to mimic the behavior.
    """
    __dict__ = dict(wrapper.__dict__)

    for attr in assigned:
        __dict__[attr] = getattr(wrapped, attr)

    __dict__['__wrapped__'] = wrapped

    # Use the metaclass of the wrapped class
    return wrapped.__class__(wrapped.__name__, (wrapped,), __dict__)


def class_wraps(wrapped, assigned=CLASS_WRAPPER_ASSIGNMENTS):
    """Decorator factory to apply create_class_wrapper() to a wrapper class.

    Return a decorator that invokes create_class_wrapper() with the decorated
    class as the wrapper argument and the arguments to class_wraps() as the
    remaining arguments. Default arguments are as for create_class_wrapper().
    This is a convenience function to simplify applying partial() to
    create_class_wrapper().
    """
    return functools.partial(create_class_wrapper, wrapped=wrapped,
                             assigned=assigned)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    doctest.testfile('README.rst', optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
