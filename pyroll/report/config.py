from pyroll.core import config


@config("PYROLL_REPORT")
class Config:
    PRINT_DISK_ELEMENTS = False
    """Whether to include the distinct disk elements into the report."""
