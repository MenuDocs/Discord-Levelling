from ..abc import Cache
from ..dataclass import Guild, Member
from ..exceptions import GuildNotFound, MemberNotFound


class Memory(Cache):
    """An in memory cache utilising a dictionary"""

    def __init__(self):
        self.cache = {}

    async def get_guild(self, guild_id: int) -> Guild:
        try:
            guild = Guild(identifier=guild_id)
            raw_members = self.cache[guild_id]
            guild._raw_members.append(raw_members)
            return guild
        except KeyError:
            raise GuildNotFound from None

    async def get_member(self, member_id: int, guild_id: int = None) -> Member:
        if guild_id:
            try:
                guild: Guild = await self.get_guild(guild_id=guild_id)
                member: Member = next(
                    i for i in guild.members if i.identifier == member_id
                )
                return member
            except GuildNotFound:
                raise MemberNotFound from None
            except KeyError:
                raise MemberNotFound from None
            except StopIteration:
                raise MemberNotFound

        try:
            return self.cache[member_id]
        except KeyError:
            raise MemberNotFound from None

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        if guild_id:
            guild = self.cache.get(guild_id)
            if not guild:
                self.cache[guild_id] = {}
            self.cache[guild_id][member_id] = data
        else:
            self.cache[member_id] = data
