from dataclasses import dataclass
from typing import Protocol, List

import attr


class Datastore(Protocol):
    """A base interface for datastores"""

    __slots__ = ()

    async def fetch_guild(self, guild_id: int) -> dict:
        """Returns the associated guilds data"""
        raise NotImplementedError

    async def fetch_member(self, member_id: int, guild_id: int = None) -> dict:
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


class Cache(Protocol):
    """A base interface for cache's"""

    __slots__ = ()

    async def get_guild(self, guild_id: int) -> dict:
        """Returns the associated guilds data"""
        raise NotImplementedError

    async def get_member(self, member_id: int, guild_id: int = None) -> dict:
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


@attr.s(slots=True)
class Member(object):
    identifier: int = attr.ib(hash=True)  # Think member.id
    xp: int = attr.ib()
    guild_id: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
        kw_only=True,
    )

    @xp.validator
    def _validate_positive(self, attr, value):
        if value < 0:
            raise ValueError("XP must be positive")


@attr.s
class Guild:
    identifier: int = attr.ib(hash=True)  # Think guild.id
    members: List[Member] = attr.ib()
