import logging
from pathlib import Path

from .report import report as report_func
from pyroll.cli import State
import click
from .config import Config

DEFAULT_REPORT_FILE = "report.html"


@click.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_REPORT_FILE, show_default=True
)
@click.option(
    "-d/-nd", "--print-disk-elements/--no-print-disk-elements",
    help="Whether to print the disk elements in the report "
         "(overrides the PRINT_DISK_ELEMENTS config value, the default is to not override the config).",
)
@click.pass_obj
def report(state: State, file: Path, print_disk_elements):
    """Generates a HTML report from the simulation results and writes it to FILE."""
    log = logging.getLogger(__name__)

    if print_disk_elements is not None:
        Config.PRINT_DISK_ELEMENTS = print_disk_elements

    rendered = report_func(state.sequence)

    file.write_text(rendered, encoding='utf-8')
    log.info(f"Wrote report to: {file.absolute()}")
