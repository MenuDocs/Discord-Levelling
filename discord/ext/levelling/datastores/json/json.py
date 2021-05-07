import json

import aiofiles

from discord.ext.levelling.abc import Datastore
from discord.ext.levelling.exceptions import GuildNotFound, MemberNotFound


class Json(Datastore):
    """This class **only** exists for testing purposes. Don't use it"""

    async def fetch_guild(self, guild_id: int) -> dict:
        data = await self._read()
        try:
            return data[guild_id]
        except AttributeError:
            raise GuildNotFound

    async def fetch_member(self, member_id: int, guild_id: int = None) -> dict:
        if guild_id:
            try:
                guild = await self.fetch_guild(guild_id=guild_id)
                return guild[member_id]
            except GuildNotFound as exc:
                raise MemberNotFound from exc
            except AttributeError:
                raise MemberNotFound

        data = await self._read()
        try:
            return data[member_id]
        except AttributeError:
            raise MemberNotFound

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

    @staticmethod
    async def _read() -> dict:
        async with aiofiles.open("store.json", "r") as f:
            # noinspection PyTypeChecker
            return json.loads(await f.readlines())

    @staticmethod
    async def _write(data: dict) -> None:
        async with aiofiles.open("store.json", "w") as f:
            await f.write(json.dumps(data, indent=4))
