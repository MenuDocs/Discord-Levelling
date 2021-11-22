from typing import List, Dict, Optional

import attr


@attr.s(slots=True)
class LevellingMember:
    """A generic ``attrs`` dataclass representing a ``discord.LevellingMember``

    Parameters
    ----------
    id : int
        -> ``discord.Member.id``
    xp : int
        The total xp this LevellingMember has
    guild_id : int, Optional
        Which guild this LevellingMember is attached to.
        If this is null it means levels are stored
        globally rather then per guild
    """

    id: int = attr.ib(hash=True, eq=True)  # Think member.id
    xp: int = attr.ib(eq=False, default=0)
    guild_id: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
        kw_only=True,
        eq=False,
    )
    level: Optional[int] = attr.ib(default=None)

    @xp.validator
    def _validate_positive(self, attr, value):
        if value < 0:
            raise ValueError("XP must be positive")


@attr.s
class LevellingGuild:
    """A generic ``attrs`` dataclass representing a ``discord.LevellingGuild``

    One of ``members`` | ``raw_members`` are **required** to build
    a LevellingGuild, however this is not checked/enforced

    Parameters
    ----------
    id : int
        -> ``discord.Guild.id``
    members: List[LevellingMember], optional
        The members internally associated with this guild

    Other Parameters
    ----------------
    raw_members : dict, Optional
        A Dict of all the members in this guild. This
        will get lazily built into ``members`` when required
    """

    id: int = attr.ib(hash=True)  # Think guild.id
    _members: List[LevellingMember] = attr.ib(default=attr.Factory(list))
    _raw_members: Dict = attr.ib(default=attr.Factory(dict))

    @property
    def members(self) -> List[LevellingMember]:
        if not bool(self._members):
            for k, v in self._raw_members.items():
                # k id, v actual data
                self._members.append(LevellingMember(**v))

        return self._members
