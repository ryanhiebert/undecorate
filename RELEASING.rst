Releasing undecorate
====================

1. Bump the version in ``setup.py``.
2. Test it with ``tox``.
3. Make sure the changelog is up-to-date.
4. Tag the release commit with the version.
5. Build and upload.


How to build and upload
-----------------------

.. code-block:: sh

    python setup.py sdist upload -r pypi
    python setup.py bdist_wheel upload -r pypi


Further Reading
---------------

* https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
