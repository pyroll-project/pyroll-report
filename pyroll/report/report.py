import datetime
import os

import jinja2
from pathlib import Path
import platform

from pyroll.core import PassSequence
from pyroll.report.pluggy import plugin_manager

from typing import Union, TextIO

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent, encoding="utf-8")
)


def report(pass_sequence: PassSequence) -> str:
    """
    Render an HTML report from the specified pass sequence.

    :param pass_sequence: PassSequence instance to take the data from
    :returns: generated HTML code as string
    """

    template = _env.get_template("main.html")

    displays = plugin_manager.hook.unit_display(unit=pass_sequence, level=1)

    return template.render(
        timestamp=datetime.datetime.now().isoformat(timespec="seconds"),
        platform=f"{platform.node()} ({platform.platform()}, {platform.python_implementation()} {platform.python_version()})",
        displays=displays,
    )


def report_to(pass_sequence: PassSequence, file: Union[str, os.PathLike, TextIO]) -> int:
    """
    Render an HTML report from the specified pass sequence and save it directly to a file.

    :param pass_sequence: PassSequence instance to take the data from
    :param file: a str representing a path, a path-like object, or a file-like object with write permissions
    to write the report to
    :returns: the number of written bytes
    """

    result = report(pass_sequence)

    try:
        return file.write(result)

    except AttributeError:
        path = Path(file)
        return path.write_text(result)
