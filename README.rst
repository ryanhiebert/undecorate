undecorate
==========

Let your decorations be undone

Installation
------------

.. code-block:: sh

    $ pip install undecorate

Usage
-----

.. code-block:: pycon

    >>> from undecorate import unwrap, unwrappable
    >>>
    >>> @unwrappable
    ... def pack(func):
    ...     def wrapper(args, kwargs):
    ...        return func(*args, **kwargs)
    ...     return wrapper
    ...
    >>> @pack
    ... def myfunc(a, b=None, c=None):
    ...     return (a, b, c)
    ...
    >>> myfunc('a', b='b')
    Traceback (most recent call last):
        ...
    TypeError: wrapper() got an unexpected keyword argument 'b'
    >>>
    >>> unwrap(myfunc)('a', b='b')
    ('a', 'b', None)
