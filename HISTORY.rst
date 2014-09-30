0.2
+++

* Add ``create_class_wrapper`` and ``class_wraps``.
* Internally use ``__wrapped__`` to match Python 3.2+.
* Add backport versions of functools ``wraps`` and ``update_wrapper``.
  They wrap the stdlib versions, and ensure that ``__wrapped__`` is set.


0.1 (2014-09-04)
++++++++++++++++

* Initial Release
* ``unwrappable`` and ``unwrap`` functions
