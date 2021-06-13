from dataclasses import dataclass


@dataclass
class Options:
    per_guild: bool = True
    ignore_dms: bool = True
    xp_increase_amount: int = 50
