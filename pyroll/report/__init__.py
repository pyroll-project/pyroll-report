from .report import report
from pyroll.report.pluggy import plugin_manager

from . import hookspecs

plugin_manager.add_hookspecs(hookspecs)

from . import unit_display

import importlib.util

CLI_INSTALLED = bool(importlib.util.find_spec("pyroll.cli"))

if CLI_INSTALLED:
    from . import cli
