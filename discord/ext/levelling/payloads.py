from .dataclass import Member


class LevelUpPayload:
    """This class represents the dispatched payload when a Member levels up"""

    def __init__(self, member: Member, level: int):
        self.member = member
        self.level = level
