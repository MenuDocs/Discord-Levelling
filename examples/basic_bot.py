import os

import discord
from discord.ext import commands
from levelling import Level, LevelUpPayload


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = Level(self)

    async def on_ready(self):
        print(f"-----\nLogged in as: {self.user.name} : {self.user.id}\n-----")

    async def on_message(self, message):
        leveled_up = await self.level.propagate(message)
        if leveled_up:
            await self.on_level_up(leveled_up)

        await self.process_commands(message)

    async def on_level_up(self, payload: LevelUpPayload):
        # This is triggered when a LevellingMember levels up
        member = payload.guild.get_member(payload.member.id)
        embed = discord.Embed(
            title=f"`{member.display_name}` has leveled up to level `{payload.level}`!"
        )
        await payload.channel.send(embed=embed)


bot = Bot(command_prefix="!", intents=discord.Intents.all())


@bot.command()
async def leaderboard(ctx):
    leaderboard_members = await bot.level.leaderboard()
    desc = "\n".join(f"<@{m.id}> - level `{m.level}`" for m in leaderboard_members)

    await ctx.send(f"Here's our leaders!\n---\n\n{desc}")


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    bot.run(token)
