import functools
import os
import sys
from typing import List

import aiosqlite as aiosqlite

from levelling.abc import Datastore
from levelling.dataclass import LevellingGuild, LevellingMember
from levelling.exceptions import MemberNotFound, GuildNotFound


def ensure_struct(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        await Sqlite._initialize(args[0].db)
        return await func(*args, **kwargs)

    return wrapped


# noinspection SqlNoDataSourceInspection,SqlResolve
class Sqlite(Datastore):
    """A simplistic, serverless SQL implementation of the Datastore Protocol"""

    _initialized = False

    def __init__(self):
        # TODO Allow customization of storage location
        self.cwd = self._get_path()

        self.db = os.path.join(self.cwd, "datastore.db")

    async def fetch_guild(self, guild_id: int) -> LevellingGuild:
        members = await self.fetch_all_members(guild_id=guild_id)
        if not bool(members):
            # Since guilds dont have a table, its based off members
            raise GuildNotFound

        return LevellingGuild(id=guild_id, members=members)

    @ensure_struct
    async def fetch_member(
        self, member_id: int, guild_id: int = None
    ) -> LevellingMember:
        if guild_id:
            async with aiosqlite.connect(self.db) as db:
                async with db.execute(
                    "SELECT * FROM LevellingMember "
                    " WHERE guild_id=:guild_id AND id=:id",
                    {
                        "guild_id": guild_id,
                        "id": member_id,
                    },
                ) as cursor:
                    value = await cursor.fetchone()
                    if not value:
                        raise MemberNotFound

                    return LevellingMember(id=value[0], xp=value[1], guild_id=value[2])

        else:
            # No guild, so just search by id
            async with aiosqlite.connect(self.db) as db:
                async with db.execute(
                    "SELECT * FROM LevellingMember WHERE id=:identifer",
                    {
                        "id": member_id,
                    },
                ) as cursor:
                    value = await cursor.fetchone()
                    if not value:
                        raise MemberNotFound

                    return LevellingMember(id=value[0], xp=value[1])

    @ensure_struct
    async def set_member(
        self, member_id: int, data: dict, guild_id: int = None
    ) -> None:
        async with aiosqlite.connect(self.db) as db:
            await db.execute(
                "INSERT INTO LevellingMember "
                "   VALUES (:id, :xp, :guild_id) "
                "ON CONFLICT(id) "
                "   DO UPDATE "
                "   SET xp=:xp",
                {
                    "id": member_id,
                    "xp": data.get("xp", 0),
                    "guild_id": guild_id,
                },
            )
            await db.commit()

    @ensure_struct
    async def fetch_all_members(self, guild_id: int = None) -> List[LevellingMember]:
        """Used internally to populate the LevellingGuild"""
        if guild_id:
            async with aiosqlite.connect(self.db) as db:
                async with db.execute(
                    "SELECT (id, xp, guild_id) FROM LevellingMember "
                    " WHERE guild_id=:guild_id",
                    {
                        "guild_id": guild_id,
                    },
                ) as cursor:
                    values = await cursor.fetchall()
                    if not values:
                        return []

                    data = []
                    for value in values:
                        data.append(
                            LevellingMember(id=value[0], xp=value[1], guild_id=guild_id)
                        )

                    return data
        else:
            async with aiosqlite.connect(self.db) as db:
                async with db.execute("SELECT * FROM LevellingMember") as cursor:
                    values = await cursor.fetchall()
                    if not values:
                        return []

                    data = []
                    for value in values:
                        data.append(
                            LevellingMember(id=value[0], xp=value[1], guild_id=guild_id)
                        )

                    return data

    @staticmethod
    async def _initialize(db) -> None:
        """A static method used to make sure the relevant tables exist"""
        if Sqlite._initialized:
            # We are initialized
            return

        async with aiosqlite.connect(db) as db:
            async with db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='LevellingMember'"
            ) as cursor:
                if not await cursor.fetchone():
                    await db.execute(
                        "CREATE TABLE LevellingMember ("
                        "   id number NOT NULL PRIMARY KEY, "
                        "   xp number NOT NULL,"
                        "   guild_id number"
                        ")"
                    )

                    await db.execute(
                        "CREATE UNIQUE INDEX id_index ON LevellingMember(id)"
                    )
                    await db.execute(
                        "CREATE UNIQUE INDEX guild_index ON LevellingMember(guild_id)"
                    )
                    await db.execute(
                        "CREATE UNIQUE INDEX shared_index ON LevellingMember(id, guild_id)"
                    )

                    await db.commit()

        Sqlite._initialized = True

    @staticmethod
    def _get_path() -> str:
        return os.path.dirname(sys.argv[0])
