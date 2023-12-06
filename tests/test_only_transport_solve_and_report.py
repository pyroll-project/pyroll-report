import logging
import webbrowser
from pathlib import Path
from pyroll.core import Profile, Roll, RollPass, Transport, RoundGroove, CircularOvalGroove, PassSequence, Rotator, \
    root_hooks
from pyroll.report import report


def equivalent_width(self: RollPass.OutProfile, cycle):
    if cycle:
        return None

    return self.roll_pass.in_profile.equivalent_width * self.roll_pass.draught ** -0.5


def test_only_transport_solve_and_report(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")
    with RollPass.OutProfile.equivalent_width(equivalent_width):

        root_hooks.add(RollPass.OutProfile.equivalent_width)
        root_hooks.add(Rotator.OutProfile.equivalent_width)

        in_profile = Profile.round(
            diameter=30e-3,
            temperature=1200 + 273.15,
            strain=0,
            material=["C45", "steel"],
            flow_stress=100e6,
            cross_section_area_deviation=3,
        )

        sequence = PassSequence(
            [

                Transport(
                    label="",
                    duration=1,
                    disk_element_count=3,
                ),
                Rotator(
                    label="",
                    rotation=90,
                    duration=0,
                ),
                Transport(
                    label="",
                    duration=1,
                )
            ]
        )

        try:
            sequence.solve(in_profile)
        finally:
            print("\nLog:")
            print(caplog.text)

    result = report(sequence)

    f = (tmp_path / "report.html")
    f.write_text(result)
    print(f)

    webbrowser.open(f.as_uri())
