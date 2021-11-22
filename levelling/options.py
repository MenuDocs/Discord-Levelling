import attr


@attr.s(slots=True)
class Options:
    """
    The levelling instance's options

    Parameters
    ----------
    per_guild: bool
        Whether levelling is per guild or global.

        Per guild by default.
    ignore_dms: bool
        Whether or not to ignore messages in dms as
        part of the levelling system.

        Default is True, so messages don't count as xp
    ignore_bots: bool
        Are bots also doing levelling?

        Default is no
    xp_base_increase_amount: int
        How much xp each message is worth as a base

        Logic is ``math.floor(random.random() * 10) + xp_base_increase_amount``
    """

    per_guild: bool = attr.ib(default=True, validator=attr.validators.instance_of(bool))
    ignore_dms: bool = attr.ib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    ignore_bots: bool = attr.ib(
        default=True, validator=attr.validators.instance_of(bool)
    )
    xp_base_increase_amount: int = attr.ib(
        default=5, validator=attr.validators.instance_of(int)
    )
