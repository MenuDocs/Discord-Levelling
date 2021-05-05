from typing import Protocol, NoReturn


class Datastore(Protocol):
    """A base interface for datastores"""

    __slots__ = ()


class Cache(Protocol):
    """A base interface for cache's"""

    __slots__ = ()

    async def get_guild(self, guild_id) -> dict:
        """Returns the associated guilds data"""
        raise NotImplementedError

    async def get_member(self, member_id, guild_id) -> dict:
        """Returns the associated member data"""
        raise NotImplementedError

    async def set_guild(self, guild_id, data=None) -> NoReturn:
        """Create a guild in cache

        Also store any data that might be
        required upon initial creation
        """
        raise NotImplementedError

    async def set_member(self, member_id, guild_id, data=None) -> NoReturn:
        """Create a member within the cache

        Store any additional data on creation
        """
        raise NotImplementedError

    async def update_member(self, member_id, guild_id, data) -> NoReturn:
        """Update a members data within cache"""
        raise NotImplementedError
