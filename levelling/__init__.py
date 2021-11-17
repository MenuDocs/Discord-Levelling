__version__ = "0.1.1"

import logging
from collections import namedtuple

from levelling.level import Level
from levelling.payloads import LevelUpPayload

logging.getLogger(__name__).addHandler(logging.NullHandler())
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=1, micro=1, releaselevel="alpha", serial=0)
