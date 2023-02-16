from pyroll.report.pluggy import plugin_manager

from . import units

plugin_manager.register(units)

from . import plots

plugin_manager.register(plots)

from . import format

plugin_manager.register(format)

from . import format_special_numbers

plugin_manager.register(format_special_numbers)

from . import format_guards

plugin_manager.register(format_guards)

from ..unit_display import properties

plugin_manager.register(properties)
