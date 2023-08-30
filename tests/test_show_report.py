import pyroll.core as pr
import pytest

from pyroll.report.report import show_report

IN_PROFILE = pr.Profile.round(
    diameter=4e-3,
    strain=0,
    flow_stress=lambda self: 100e6,
)

SEQUENCE = pr.PassSequence([
    pr.RollPass(
        roll=pr.Roll(
            groove=pr.CircularOvalGroove(r1=1e-3, r2=5e-3, depth=1e-3),
            nominal_radius=100e-3
        ),
        gap=1e-3,
        velocity=1,
    ),
])

SEQUENCE.solve(IN_PROFILE)


def test_str():
    f = show_report(SEQUENCE)

    assert f.exists()
