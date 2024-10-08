import logging as _logging
from typing import Final

from .client import *
from .misc import *

__version__: Final[str] = "2.0"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
