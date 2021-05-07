import discord
from discord.ext import commands
from discord.ext.levelling import Level

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot.level = Level()


@bot.event
async def on_ready():
    # On ready, print some details to standard out
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----")


@bot.event
async def on_message(message):
    await bot.level.propagate(message)
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run("NTY2MTMwNjk4OTM1NTk5MTA0.Xb5zvw.JiKInSTwOynpE5y8j335em5X6kI")
