Discord Levelling
---

A package built for discord.py developers who want to
easily and seamlessly integrate a levelling system into
their bots.

#### Key features
 - Easy database integration for *any* database system
 - Fully tested
 - Highly customizable 
 - Plug & Play

---

## Example usage

```python
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
        member = payload.guild.get_member(payload.member.id)
        embed = discord.Embed(

            title=f"`{member.display_name}` has leveled up to level `{payload.level}`!"

        )
        await payload.channel.send(embed=embed)


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    Bot(command_prefix="!", intents=discord.Intents.all()).run(token)
```

## Documentation | Examples | Support

For documentation and examples, [see here](https://discord-ext-levelling.readthedocs.io/en/latest/)

Join the MenuDocs' discord server for support with this package!
- https://discord.gg/menudocs

or dm us on twitter!
- https://twitter.com/menudocs
