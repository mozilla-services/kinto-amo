CHANGELOG
=========

1.0.0 (2018-02-07)
------------------

- Pass application ID and version to amo2kinto code when generating blocklist.xml. (#23)


0.4.0 (2017-07-05)
------------------

**New features**

- Add support for cache control headers (``If-None-Match`` and ``If-Modified-Since``) (fixes #21)

0.3.0 (2016-10-27)
------------------

- Add the plugin version in the capability. (#15)
- Enable creation of preview XML files from other collections. (#18)


0.2.0 (2016-05-19)
------------------

- Update to ``kinto.core`` for compatibility with Kinto 3.0. This
  release is no longer compatible with Kinto < 3.0, please upgrade!


0.1.1 (2016-05-06)
------------------

- Missing commit in previous release.


0.1.0 (2016-05-06)
------------------

**New features**

- Supports metrics in the URL (#6)
- Add a view to render the XML Blocklists file in versions 1, 2 and 3 (#3)
