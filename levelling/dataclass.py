from typing import List, Dict

import attr


@attr.s(slots=True)
class Member(object):
    """A generic ``attrs`` dataclass representing a ``discord.Member``

    Parameters
    ----------
    identifier : int
        -> ``discord.Member.id``
    xp : int
        The total xp this Member has
    guild_id : int, optional
        Which guild this Member is attached to.
        If this is null it means levels are stored
        globally rather then per guild
    """

    identifier: int = attr.ib(hash=True, eq=True)  # Think member.id
    xp: int = attr.ib(eq=False, default=0)
    guild_id: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
        kw_only=True,
        eq=False,
    )

    @xp.validator
    def _validate_positive(self, attr, value):
        if value < 0:
            raise ValueError("XP must be positive")


@attr.s
class Guild:
    """A generic ``attrs`` dataclass representing a ``discord.Guild``

    One of ``members`` | ``raw_members`` are **required** to build
    a Guild, however this is not checked/enforced

    Parameters
    ----------
    identifier : int
        -> ``discord.Guild.id``
    members: List[Member], optional
        The members internally associated with this guild

    Other Parameters
    ----------------
    raw_members : dict, optional
        A Dict of all the members in this guild. This
        will get lazily built in ``members`` when required
    """

    identifier: int = attr.ib(hash=True)  # Think guild.id
    _members: List[Member] = attr.ib(default=attr.Factory(list))
    _raw_members: Dict = attr.ib(default=attr.Factory(dict))

    @property
    def members(self) -> List[Member]:
        if not bool(self._members):
            for k, v in self._raw_members.items():
                # k id, v actual data
                self._members.append(Member(**v))

        return self._members
