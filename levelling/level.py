import math
import random
from functools import lru_cache
from typing import Optional, List

import discord

from levelling.store import Store
from levelling.caches import Memory
from levelling.options import Options
from levelling.dataclass import LevellingMember
from levelling.datastores import Sqlite
from levelling.abc import Cache, Datastore
from levelling.payloads import LevelUpPayload


class Level:
    """The main interaction point for the discord.ext.levelling package"""

    def __init__(
        self,
        bot,
        *,
        cache: Cache = None,
        datastore: Datastore = None,
        options: Options = None
    ):
        """

        Parameters
        ----------
        bot: commands.Bot
            The instance of the bot to use internally
        cache : Cache
            An instance of a class implementing the ``Cache`` interface Protocol
        datastore : Datastore
            An instance of a class implementing the ``Datastore`` interface Protocol
        options : Options
            An instance of the ``Options`` dataclass to show the options to support
        """
        self.bot = bot
        self.options = options or Options()

        cache = cache or Memory()
        datastore = datastore or Sqlite()
        self.store = Store(cache=cache, datastore=datastore)

    async def propagate(self, message: discord.Message) -> Optional[LevelUpPayload]:
        if (self.options.ignore_dms or self.options.per_guild) and not message.guild:
            # Either dm's are ignored or per guild is enabled, so ignore dm's
            # Ignore guilds atm
            return

        if self.options.ignore_bots and message.author.bot:
            return

        guild_id: int = message.guild.id if self.options.per_guild else None
        member: LevellingMember = await self.store.create_or_fetch_member(
            member_id=message.author.id, guild_id=guild_id
        )

        # Get level before xp
        current_level = self.get_level_from_xp(member.xp)

        # Add a random amount of xp with the base
        member.xp += (
            math.floor(random.random() * 10) + self.options.xp_base_increase_amount
        )

        # Get level after xp addition
        new_level = self.get_level_from_xp(member.xp)

        # Update internals
        await self.store.set_member(member)

        if current_level == new_level:
            # Do nothing, didnt level up
            return None

        # Did level up
        return LevelUpPayload(member=member, level=new_level, channel=message.channel)

    async def leaderboard(self, guild_id: int = None) -> List[LevellingMember]:
        """
        Returns a list of members sorted by level.

        Parameters
        ----------
        guild_id: int
            The guild to work with

        Returns
        -------
        List[LevellingMember]
            The sorted list of members
        """
        guild_id: int = guild_id if self.options.per_guild else None
        members = await self.store.datastore.fetch_all_members(guild_id)
        data = []
        for member in members:
            member.level = self.get_level_from_xp(member.xp)
            data.append(member)

        return sorted(data, key=lambda x: x.level)

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
            The LevellingMember's level
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
