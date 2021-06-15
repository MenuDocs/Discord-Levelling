import math
import random
from functools import lru_cache

from attr import asdict

from .caches import Memory
import discord.ext.levelling.options
from .abc import Cache, Datastore
from .dataclass import Member
from .exceptions import MemberNotFound
from .datastores.json import Json
from .options import Options
from .payloads import LevelUpPayload


class Level:
    """The main interaction point for the discord.ext.levelling package"""

    def __init__(
        self,
        bot,
        *,
        cache: Cache = None,
        data_store: Datastore = None,
        options: Options = None
    ):
        """

        Parameters
        ----------
        bot: commands.Bot

        cache : Cache
            An instance of a class implementing the ``Cache`` interface Protocol
        data_store : Datastore
            An instance of a class implementing the ``Datastore`` interface Protocol
        options : Options
            An instance of the ``Options`` dataclass to show the options to support
        """
        self.bot = bot
        self.cache = cache or Memory()
        self.data_store = data_store or Json()
        self.options = options or Options()

    async def propagate(self, message: discord.Message) -> None:
        if (self.options.ignore_dms or self.options.per_guild) and not message.guild:
            # Either dm's are ignored or per guild is enabled, so ignore dm's
            # Ignore guilds atm
            return

        member = Member(identifier=message.author.id, guild_id=message.guild.id)
        guild_id: int = message.guild.id if self.options.per_guild else None
        try:
            member: Member = await self.cache.get_member(
                member_id=message.author.id, guild_id=guild_id
            )
        except MemberNotFound:
            try:
                member: Member = await self.data_store.fetch_member(
                    member_id=message.author.id, guild_id=guild_id
                )
            except MemberNotFound:
                pass

        # Get level before xp
        current_level = self.get_level_from_xp(member.xp)

        # Add a random amount of xp with the base
        member.xp += (
            math.floor(random.random() * 10) + self.options.xp_base_increase_amount
        )

        # Get level after xp addition
        new_level = self.get_level_from_xp(member.xp)

        # Update internals
        await self.data_store.set_member(
            member_id=member.identifier, data=asdict(member), guild_id=member.guild_id
        )
        await self.cache.set_member(
            member_id=member.identifier, data=asdict(member), guild_id=member.guild_id
        )

        if current_level == new_level:
            # Do nothing, didnt level up
            return

        # Did level up
        self.bot.dispatch(
            "level_up",
            LevelUpPayload(member=member, level=new_level, channel=message.channel),
        )

    @lru_cache
    def get_level_xp_amount(self, level: int) -> int:
        """
        Returns the amount of xp required
        for the next level

        Parameters
        ----------
        level: int
            The members current level

        Returns
        -------
        int
            Required xp for the next level
        """
        return 5 * (level ** 2) + 50 * level + 100

    @lru_cache
    def get_level_from_xp(self, xp: int) -> int:
        """
        Given a member, extract there level from the
        amount of xp they currently have

        Parameters
        ----------
        xp: int
            The xp amount to get a level for

        Returns
        -------
        int
            The Member's level
        """
        level = 0
        remaining_xp = xp
        while remaining_xp >= self.get_level_xp_amount(level):
            remaining_xp -= self.get_level_xp_amount(level)
            level += 1
        return level

    @lru_cache
    def get_remaining_xp(self, current_level: int, xp: int) -> int:
        """
        Calculates the required amount of xp left to
        achieve the next level from the current level

        Parameters
        ----------
        current_level : int
            The Members current level
        xp : int
            The members current xp

        Returns
        -------
        int
            The amount of xp required to get to the next level
        """
        xp_to_next_level = 0
        for i in range(current_level):
            xp_to_next_level += self.get_level_xp_amount(current_level)
        return xp - xp_to_next_level

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
