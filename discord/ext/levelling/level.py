import discord

from .caches import Memory
from .options import Options
from .abc import Cache, Datastore
from .exceptions import MemberNotFound


class Level:
    """The main interaction point for the discord.ext.levelling package"""

    def __init__(
        self,
        *,
        cache: Cache = None,
        data_store: Datastore = None,
        options: Options = None
    ):
        """

        Parameters
        ----------
        cache : Cache
            An instance of a class implementing the ``Cache`` interface Protocol
        data_store : Datastore
            An instance of a class implementing the ``Datastore`` interface Protocol
        options : Options
            An instance of the ``Options`` dataclass to show the options to support
        """
        self.cache = cache or Memory()
        self.data_store = data_store
        self.options = options

    async def propagate(self, message: discord.Message) -> None:
        if (self.options.ignore_dms or self.options.per_guild) and not message.guild:
            # Either dm's are ignored or per guild is enabled, so ignore dm's
            return

    @staticmethod
    async def from_store(data_store: Datastore):
        """
        Creates and returns a Level instance from
        a given ``Datastore``

        Parameters
        ----------
        data_store : Datastore
            The datastore to restore from

        Returns
        -------
        Level
            A ``Level`` instance built from a given ``Datastore``
        """
