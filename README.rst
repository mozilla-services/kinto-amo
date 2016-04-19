==============
Kinto AMO View
==============

.. image:: https://img.shields.io/travis/mozilla-services/kinto-amo/master.svg
        :target: https://travis-ci.org/mozilla-services/kinto-amo

.. image:: https://img.shields.io/pypi/v/kinto-amo.svg
        :target: https://pypi.python.org/pypi/kinto-amo

.. image:: https://coveralls.io/repos/mozilla-services/kinto-amo/badge.svg?branch=master
        :target: https://coveralls.io/r/mozilla-services/kinto-amo

Return an XML views of the blocklists buckets compatible with the
previous AMO one.


Install
=======

::

    pip install kinto-amo


Setup
=====

In the Kinto project settings

.. code-block:: ini

    kinto.includes = kinto_amo

