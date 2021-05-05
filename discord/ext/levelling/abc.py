from typing import Protocol


class Datastore(Protocol):
    """A base interface for datastores"""

    __slots__ = ()


class Cache(Protocol):
    """A base interface for cache's"""

    __slots__ = ()
