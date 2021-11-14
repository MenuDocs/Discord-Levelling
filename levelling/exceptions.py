from discord import DiscordException


class LevellingError(DiscordException):
    """Base Levelling exception class"""

    pass


class MemberNotFound(LevellingError):
    """Raised internally when a member doesn't exist within the cache"""

    pass


class GuildNotFound(LevellingError):
    """Raised internally when a guild doesn't exist within the cache"""

    pass
