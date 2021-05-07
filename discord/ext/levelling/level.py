import discord

from discord.ext.levelling.caches import Memory
from discord.ext.levelling.options import Options
from discord.ext.levelling.abc import Cache, Datastore, Member
from discord.ext.levelling.exceptions import MemberNotFound

from discord.ext.levelling.datastores.json import Json


class Level:
    """The main interaction point for the discord.ext.levelling package"""

    def __init__(
        self,
        *,
        cache: Cache = None,
        data_store: Datastore = None,
        options: Options = None
    ):
        """

        Parameters
        ----------
        cache : Cache
            An instance of a class implementing the ``Cache`` interface Protocol
        data_store : Datastore
            An instance of a class implementing the ``Datastore`` interface Protocol
        options : Options
            An instance of the ``Options`` dataclass to show the options to support
        """
        self.cache = cache or Memory()
        self.data_store = data_store or Json()
        self.options = options or Options()

    async def propagate(self, message: discord.Message) -> None:
        if (self.options.ignore_dms or self.options.per_guild) and not message.guild:
            # Either dm's are ignored or per guild is enabled, so ignore dm's
            return

        member = Member(identifier=message.author.id, xp=0)
        guild_id: int = message.guild.id if self.options.per_guild else None
        try:
            member_data = await self.cache.get_member(
                member_id=message.author.id, guild_id=guild_id
            )
            member = Member(
                identifier=member_data["identifier"],
                xp=member_data["xp"],
                guild_id=member_data["guild_id"],
            )
        except MemberNotFound:
            try:
                member_data = await self.data_store.fetch_member(
                    member_id=message.author.id, guild_id=guild_id
                )
                member = Member(
                    identifier=member_data["identifier"],
                    xp=member_data["xp"],
                    guild_id=member_data["guild_id"],
                )
            except MemberNotFound:
                pass

    async def increase_xp(self, member: Member):
        member.xp += 15

    @staticmethod
    async def from_store(data_store: Datastore):
        """
        Creates and returns a Level instance from
        a given ``Datastore``

        Parameters
        ----------
        data_store : Datastore
            The datastore to restore from

        Returns
        -------
        Level
            A ``Level`` instance built from a given ``Datastore``
        """
