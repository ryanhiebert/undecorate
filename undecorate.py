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

from functools import wraps


def unwrappable(decorator):
    """Make a decorator able to be un-decorated.

    This meta-decorator takes a decorator, and returns a new decorator
    that allows the decoration to be used by unwrap().
    """
    @wraps(decorator)
    def wrapper(decoration):
        decorated = decorator(decoration)
        decorated.__decoration__ = decoration
        return decorated
    return wrapper


def unwrap(wrapped):
    """Remove all wrappers from this decorated object."""
    while True:
        decoration = getattr(wrapped, '__decoration__', None)
        if decoration is None:
            return wrapped
        wrapped = decoration


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
    doctest.testfile('README.rst', optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
