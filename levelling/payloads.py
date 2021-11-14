import discord

from levelling.dataclass import Member


class LevelUpPayload:
    """
    This class represents the dispatched payload when a Member levels up

    Attributes
    ----------
    member : Member
        The Member who levelled up.

        Note this is this packages member, you will need to fetch the
        member object yourself to get a ``discord.Member`` object
    level : int
        The new level of the Member levelling up
    channel : discord.TextChannel
        The channel the message that triggered a level up occurred in
    guild : discord.Guild
        The Guild for the member levelling up

    Notes
    -----
    This is not initialized by you.
    """

    __slots__ = ("member", "level", "channel", "guild")

    def __init__(self, member: Member, level: int, channel: discord.TextChannel):
        self.member: Member = member
        self.level: int = level
        self.channel: discord.TextChannel = channel
        self.guild: discord.Guild = self.channel.guild
