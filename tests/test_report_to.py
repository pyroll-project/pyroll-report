import pyroll.core as pr
import pytest

from pyroll.report.report import report_to

IN_PROFILE = pr.Profile.round(
    diameter=4e-3,
    strain=0,
    flow_stress=100e6,
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


def test_str(tmp_path):
    f = tmp_path / "report.html"

    report_to(SEQUENCE, str(f))

    assert f.exists()


def test_path(tmp_path):
    f = tmp_path / "report.html"

    report_to(SEQUENCE, f)

    assert f.exists()


def test_file_object(tmp_path):
    f = tmp_path / "report.html"

    report_to(SEQUENCE, f.open("w", encoding="utf-8"))

    assert f.exists()


def test_file_object_bin(tmp_path):
    f = tmp_path / "report.html"
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        report_to(SEQUENCE, f.open("wb"))
