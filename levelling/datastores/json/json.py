import json
import os
import sys

from levelling.abc import Datastore
from levelling.dataclass import LevellingGuild, LevellingMember
from levelling.exceptions import GuildNotFound, MemberNotFound


class Json(Datastore):
    """This class **only** exists for testing purposes. Don't use it

    Seriously its bad, its blocking, don't use it.
    """

    def __init__(self):
        self.path = self._get_path()

    async def fetch_guild(self, guild_id: int) -> LevellingGuild:
        data = await self._read()
        try:
            return LevellingGuild(id=guild_id, raw_members=data[str(guild_id)])
        except KeyError:
            raise GuildNotFound from None

    async def fetch_member(
        self, member_id: int, guild_id: int = None
    ) -> LevellingMember:
        if guild_id:
            try:
                guild = await self.fetch_guild(guild_id=guild_id)
                member: LevellingMember = next(
                    i for i in guild.members if i.id == member_id
                )
                return member
            except GuildNotFound:
                raise MemberNotFound from None
            except KeyError:
                raise MemberNotFound from None
            except StopIteration:
                raise MemberNotFound

        data = await self._read()
        try:
            return data[str(member_id)]
        except KeyError:
            raise MemberNotFound from None

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        file_data = await self._read()
        member_id = str(member_id)
        if guild_id:
            guild_id = str(guild_id)
            if guild_id not in file_data:
                file_data[guild_id] = {}
            file_data[guild_id][member_id] = data

        else:
            file_data[member_id] = data

        await self._write(file_data)

    async def _read(self) -> dict:
        with open(os.path.join(self.path, "store.json"), "r") as f:
            # noinspection PyTypeChecker
            return json.load(f)

    async def _write(self, data: dict) -> None:
        with open(os.path.join(self.path, "store.json"), "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def _get_path() -> str:
        return os.path.dirname(sys.argv[0])
