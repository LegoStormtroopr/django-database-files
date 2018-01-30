django-database-files
=====================

.. image:: https://travis-ci.org/LegoStormtroopr/django-database-files.svg?branch=master
    :target: https://travis-ci.org/LegoStormtroopr/django-database-files

``django-database-files`` is a storage system for Django that stores files in the database.
It can act as a storage class anywhere that accepts the `Django storage API <https://docs.djangoproject.com/en/2.0/ref/files/storage/>`_.

WARNING: There are serious downsides to storing and serving static files from Django,
but there are some valid use cases.

If your Django app is behind a caching reverse proxy and you need to scale your
application servers, it may be simpler to store files in the database.

Likewise, when using systems like Heroku where no easy and persistent file system 
exists, storing files in the database can provide a quick way to add file management.


Requires:

  * Django 1.11 or above only
  * Python 3.5 or above only

Installation
------------

    $ pip install django-database-files-ny

Usage
-----

In ``settings.py``, add ``database_files`` to your ``INSTALLED_APPS`` and add this line::

    DEFAULT_FILE_STORAGE = 'database_files.storage.DatabaseStorage'

In your ``urls.py`` add a path to the database files::

    url(r'^db_static/', include("database_files.urls")),

All your ``FileField`` and ``ImageField`` files will now be stored in the 
database.

Test suite
----------

    $ tox

