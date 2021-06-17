import os

import discord
from discord.ext import commands
from discord.ext.levelling import Level, LevelUpPayload


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = Level(self)

    async def on_ready(self):
        print(f"-----\nLogged in as: {self.user.name} : {self.user.id}\n-----")

    async def on_message(self, message):
        await self.level.propagate(message)
        await self.process_commands(message)

    async def on_level_up(self, payload: LevelUpPayload):
        member = payload.channel.guild.get_member(payload.member.identifier)
        embed = discord.Embed(
            title=f"`{member.display_name}` has leveled up to level `{payload.level}`!"
        )
        await payload.channel.send(embed=embed)


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    Bot(command_prefix="!", intents=discord.Intents.all()).run(token)
