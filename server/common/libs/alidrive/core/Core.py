"""..."""

from .Create import Create
from .LocalCreate import LocalCreate
from .Download import Download
from .Drive import Drive
from .File import File
from .Recyclebin import Recyclebin
from .User import User
from .Video import Video


class Core(
    Create,
    LocalCreate,
    Download,
    Drive,
    User,
    File,
    Recyclebin,
    Video
):
    """..."""
