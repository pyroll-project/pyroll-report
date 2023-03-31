import logging
import subprocess
import webbrowser
from importlib.metadata import entry_points

import pytest

import pyroll.report

from click.testing import CliRunner
from pyroll.cli.program import main

commands = entry_points(group="pyroll.cli.commands")

for c in commands:
    main.add_command(c.load())

INPUT = """
from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence

in_profile = Profile.round(
    diameter=30e-3,
    temperature=1200 + 273.15,
    strain=0,
    material=["C45", "steel"],
    flow_stress=100e6
)

sequence = PassSequence([
    RollPass(
        label="Oval I",
        roll=Roll(
            groove=CircularOvalGroove(
                depth=8e-3,
                r1=6e-3,
                r2=40e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
    Transport(
        label="I => II",
        duration=1
    ),
    RollPass(
        label="Round II",
        roll=Roll(
            groove=RoundGroove(
                r1=1e-3,
                r2=12.5e-3,
                depth=11.5e-3
            ),
            nominal_radius=160e-3,
            rotational_frequency=1
        ),
        gap=2e-3,
    ),
])
"""

RUNNER = CliRunner()


@pytest.mark.skipif(not pyroll.report.CLI_INSTALLED, reason="pyroll-cli is not installed in the current environment")
def test_cli(tmp_path, monkeypatch, caplog):
    (tmp_path / "input.py").write_text(INPUT)
    caplog.set_level(logging.INFO, "pyroll")
    monkeypatch.chdir(tmp_path)

    result = RUNNER.invoke(main, ("input-py", "solve", "report"))

    print(caplog.text)

    assert result.exit_code == 0

    webbrowser.open((tmp_path / "report.html").as_uri())
