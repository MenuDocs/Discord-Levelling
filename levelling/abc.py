from typing import Protocol, List

from levelling.dataclass import LevellingMember, LevellingGuild


class Datastore(Protocol):
    """A base interface for datastores"""

    __slots__ = ()

    async def fetch_guild(self, guild_id: int) -> LevellingGuild:
        """Returns the associated guilds data"""
        raise NotImplementedError

    async def fetch_member(
        self, member_id: int, guild_id: int = None
    ) -> LevellingMember:
        """Returns the associated member data

        Where ``guild_id`` is ``None`` implies
        a global levelling storage
        """
        raise NotImplementedError

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        """Store data within the cache attached to a member

        Where ``guild_id`` is ``None`` implies
        a global levelling storage
        """
        raise NotImplementedError

    async def fetch_all_members(self, guild_id: int = None) -> List[LevellingMember]:
        """
        Returns all members for a guild, or everyone.

        Parameters
        ----------
        guild_id: int, optional
            The guild to fetch from

        Returns
        -------
        List[LevellingMember]
            A list of members sorted by level
        """
        raise NotImplementedError


class Cache(Protocol):
    """A base interface for cache's"""

    __slots__ = ()

    async def get_guild(self, guild_id: int) -> LevellingGuild:
        """Returns the associated guilds data"""
        raise NotImplementedError

    async def get_member(self, member_id: int, guild_id: int = None) -> LevellingMember:
        """Returns the associated member data

        Where ``guild_id`` is ``None`` implies
        a global levelling storage
        """
        raise NotImplementedError

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        """Store data within the cache attached to a member

        Where ``guild_id`` is ``None`` implies
        a global levelling storage
        """
        raise NotImplementedError
