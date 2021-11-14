from typing import Optional

from levelling.abc import Datastore, Cache
from levelling.dataclass import Member
from levelling.exceptions import MemberNotFound


class Store:
    """
    An abstraction layer for storage classes,
    providing easy access to data from both caches/persistent storage.
    """

    def __init__(self, *, cache: Cache, datastore: Datastore):
        self.cache = cache
        self.datastore = datastore

    async def create_or_fetch_member(self, member_id: int, guild_id: int) -> Member:
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
        Member
            The stored/cached/created member
        """
        member: Optional[Member] = None
        try:
            member: Member = await self.fetch_member(
                member_id=member_id, guild_id=guild_id
            )
        except MemberNotFound:
            member = Member(identifier=member_id, guild_id=guild_id)
        finally:
            return member

    async def fetch_member(self, member_id: int, guild_id: int) -> Member:
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
        Member
            The stored/cached member

        Raises
        ------
        MemberNotFound
            The member could not be found
        """
        member: Optional[Member] = None
        try:
            member: Member = await self.cache.get_member(
                member_id=member_id, guild_id=guild_id
            )
        except MemberNotFound:
            member: Member = await self.datastore.fetch_member(
                member_id=member_id, guild_id=guild_id
            )
        finally:
            return member
