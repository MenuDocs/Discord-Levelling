import json
import os

import aiofiles
from pathlib import Path

from discord.ext.levelling.abc import Datastore
from discord.ext.levelling.dataclass import Guild, Member
from discord.ext.levelling.exceptions import GuildNotFound, MemberNotFound


class Json(Datastore):
    """This class **only** exists for testing purposes. Don't use it

    Seriously its bad, its blocking, don't use it.
    """

    def __init__(self):
        self.path = self._get_path()

    async def fetch_guild(self, guild_id: int) -> Guild:
        data = await self._read()
        try:
            return data[guild_id]
        except KeyError:
            raise GuildNotFound from None

    async def fetch_member(self, member_id: int, guild_id: int = None) -> Member:
        if guild_id:
            try:
                guild = await self.fetch_guild(guild_id=guild_id)
                return guild[member_id]
            except GuildNotFound:
                raise MemberNotFound from None
            except KeyError:
                raise MemberNotFound from None

        data = await self._read()
        try:
            return data[member_id]
        except KeyError:
            raise MemberNotFound from None

    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        file_data = await self._read()
        if guild_id:
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

    def _get_path(self) -> str:
        return str(Path(__file__).parents[0])
