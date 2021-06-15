import discord

from .dataclass import Member


class LevelUpPayload:
    """This class represents the dispatched payload when a Member levels up"""

    def __init__(self, member: Member, level: int, channel: discord.TextChannel):
        self.member: Member = member
        self.level: int = level
        self.channel: discord.TextChannel = channel
