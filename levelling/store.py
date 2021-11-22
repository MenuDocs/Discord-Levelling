from typing import Optional

from attr import asdict

from levelling.abc import Datastore, Cache
from levelling.dataclass import LevellingMember
from levelling.exceptions import MemberNotFound


class Store:
    """
    An abstraction layer for storage classes,
    providing easy access to data from both caches/persistent storage.
    """

    def __init__(self, *, cache: Cache, datastore: Datastore):
        self.cache = cache
        self.datastore = datastore

    async def create_or_fetch_member(
        self, member_id: int, guild_id: int
    ) -> LevellingMember:
        """
        Fetches a member, creates if one can't be found.

        Parameters
        ----------
        member_id: int
            The id for the member
        guild_id: int
            The id for the guild of the member

        Returns
        -------
        LevellingMember
            The stored/cached/created member
        """
        member: Optional[LevellingMember] = None
        try:
            member: LevellingMember = await self.fetch_member(
                member_id=member_id, guild_id=guild_id
            )
        except MemberNotFound:
            member = LevellingMember(id=member_id, guild_id=guild_id)
        finally:
            return member

    async def fetch_member(self, member_id: int, guild_id: int) -> LevellingMember:
        """
        Fetches a member, errors if one can't be found.

        Parameters
        ----------
        member_id: int
            The id for the member
        guild_id: int
            The id for the guild of the member

        Returns
        -------
        LevellingMember
            The stored/cached member

        Raises
        ------
        MemberNotFound
            The member could not be found
        """
        try:
            member: LevellingMember = await self.cache.get_member(
                member_id=member_id, guild_id=guild_id
            )
        except MemberNotFound:
            try:
                member: LevellingMember = await self.datastore.fetch_member(
                    member_id=member_id, guild_id=guild_id
                )
            except MemberNotFound as e:
                raise e

        return member

    async def set_member(self, member: LevellingMember) -> None:
        """
        Stores a member in both cache and persistent storage.

        Parameters
        ----------
        member: LevellingMember
            The member to store
        """
        await self.datastore.set_member(
            member_id=member.id, data=asdict(member), guild_id=member.guild_id
        )
        await self.cache.set_member(
            member_id=member.id, data=asdict(member), guild_id=member.guild_id
        )
