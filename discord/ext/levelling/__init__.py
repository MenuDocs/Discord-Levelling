__version__ = "0.1.0"

import logging
from collections import namedtuple

from .level import Level
from .payloads import LevelUpPayload

logging.getLogger(__name__).addHandler(logging.NullHandler())
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="alpha", serial=0)
