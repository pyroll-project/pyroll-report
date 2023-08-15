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


def test_solve_and_report(tmp_path: Path, caplog):
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
                    target_filling_ratio=0.85,
                ),
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
                    target_filling_ratio=0.98,
                ),
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
