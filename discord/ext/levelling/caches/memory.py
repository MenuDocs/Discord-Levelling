from discord.ext.levelling.abc import Cache
from discord.ext.levelling.exceptions import GuildNotFound, MemberNotFound


class Memory(Cache):
    """An in memory cache utilising a dictionary"""

    def __init__(self):
        self.cache = {}

    async def get_guild(self, guild_id: int) -> dict:
        try:
            return self.cache[guild_id]
        except KeyError:
            raise GuildNotFound from None

    async def get_member(self, member_id: int, guild_id: int = None) -> dict:
        if guild_id:
            try:
                guild = await self.get_guild(guild_id=guild_id)
                return guild[member_id]
            except GuildNotFound:
                raise MemberNotFound from None
            except KeyError:
                raise MemberNotFound from None

        try:
            return self.cache[member_id]
        except KeyError:
            raise MemberNotFound from None

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        if guild_id:
            guild = self.cache.get(guild_id, {})
            guild[member_id] = data
        else:
            self.cache[member_id] = data
