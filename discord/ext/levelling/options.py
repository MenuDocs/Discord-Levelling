from dataclasses import dataclass


@dataclass
class Options:
    per_guild: bool = True
    ignore_dms: bool = True
