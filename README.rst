======
mcinfo
======

.. image:: https://coveralls.io/repos/github/randomdude999/mcinfo/badge.svg?branch=master
    :target: https://coveralls.io/github/randomdude999/mcinfo?branch=master
.. image:: https://travis-ci.org/randomdude999/mcinfo.svg?branch=master
    :target: https://travis-ci.org/randomdude999/mcinfo

A command-line tool to show information about Minecraft blocks, items and more.

Installing
----------
::

    pip install mcinfo

Usage
-----
::

    $ mcinfo stone
    [TBI]
    $ mcinfo iron_sword
    [TBI]
    $ mcinfo pig
    [TBI]
    $ mcinfo
    > nbt:cow
    { }  Entity data
        [All tags from entity]
        [All tags from mob]
        [All tags from breedable]
    > wooden_sword
    [TBI]
    > quit

Developing
----------

To get a dev environment::

    $ git clone https://github.com/randomdude999/mcinfo
    $ cd mcinfo
    $ virtualenv venv
    $ source venv/bin/activate   # Or whatever you do to activate a virtualenv
    $ pip install nose2 coverage cov-core
    $ pip install -e .

Tests
-----

Tests use nose2. Simply type ``nose2`` to run the tests. If you have
``coverage`` and ``cov-core`` installed, it will also generate an HTML
report of code coverage. You can also type ``python setup.py test`` if you
prefer that.
