Supported Storage Backends
==========================

This page *only* details storage backends shipped with the package.

Caches
------

Any class can be used for a cache assuming it implements
the ``abc.Cache`` Protocol.

However the following ship with the package:

.. module:: levelling.caches
.. autoclass:: Memory


Datastores
----------
Any class can be used for a cache assuming it implements
the ``abc.Datastore`` Protocol.

.. module:: levelling.datastores.json
.. autoclass:: Json

*This is the currently used default datastore*

.. module:: levelling.datastores
.. autoclass:: Sqlite
