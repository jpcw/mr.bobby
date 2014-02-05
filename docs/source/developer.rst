.. highlight:: bash

Developer guide
===============

Setup developer environment
---------------------------

::

    $ git clone https://github.com/jpcw/mr.bobby.git
    $ cd mrbobby
    $ virtualenv .
    $ source bin/activate
    $ python setup.py develop
    $ easy_install mr.bobby[test,development]
    $ mrbobby --help


Running tests
-------------

Easy as::

    $ make test


Making a Release
----------------

Using `zest.releaser`::

    $ bin/fullrelease
