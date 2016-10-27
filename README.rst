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

    # kinto.amo.addons = /buckets/blocklists/collections/addons
    # kinto.amo.plugins = /buckets/blocklists/collections/plugins
    # kinto.amo.gfx = /buckets/blocklists/collections/gfx
    # kinto.amo.certificates = /buckets/blocklists/collections/certificates


You can setup other blocklists for preview for instance using a prefix:

.. code-block:: ini

    kinto.includes = kinto_amo

    kinto.amo.preview.addons = /buckets/blocklists-preview/collections/addons
    kinto.amo.preview.plugins = /buckets/blocklists-preview/collections/plugins
    kinto.amo.preview.gfx = /buckets/blocklists-preview/collections/gfx
    kinto.amo.preview.certificates = /buckets/blocklists-preview/collections/certificates

    kinto.amo.staging.addons = /buckets/staging/collections/addons
    kinto.amo.staging.plugins = /buckets/staging/collections/plugins
    kinto.amo.staging.gfx = /buckets/staging/collections/gfx
    kinto.amo.staging.certificates = /buckets/staging/collections/certificates

You can then access their blocklist from the prefixed URL:

- ``/v1/blocklist/3/{3550f703-e582-4d05-9a08-453d09bdfdc6}/47.0/``
- ``/v1/preview/3/{3550f703-e582-4d05-9a08-453d09bdfdc6}/47.0/``
- ``/v1/staging/3/{3550f703-e582-4d05-9a08-453d09bdfdc6}/47.0/``
