Example Usage
=============

The below is a simplistic implementation of how
to use this package in your next discord bot.

.. code-block:: python
    :linenos:

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
            # This is triggered when a Member levels up
            member = payload.guild.get_member(payload.member.identifier)
            embed = discord.Embed(
                title=f"`{member.display_name}` has leveled up to level `{payload.level}`!"
            )
            await payload.channel.send(embed=embed)


    if __name__ == "__main__":
        token = os.getenv("TOKEN")
        Bot(command_prefix="!", intents=discord.Intents.all()).run(token)
