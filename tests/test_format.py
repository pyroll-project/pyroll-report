import webbrowser

import pytest
from pyroll.core import Transport
from shapely import Point

import pyroll.report
import numpy as np

from pyroll.report import Config
from pyroll.report.unit_display.properties import DoNotPrint


def _test_format(name: str, value: object, expected: str):
    result = pyroll.report.plugin_manager.hook.property_format(value=value, name=name)
    print(result)
    assert result == expected


def test_int():
    _test_format("", 42, "42")


def test_bool():
    _test_format("", True, "True")


def test_float():
    _test_format("", np.pi, "3.142e+00")
    _test_format("", np.pi * 1e3, "3.142e+03")
    _test_format("", np.pi * 1e2, "314.159e+00")
    _test_format("", np.pi / 1e1, "314.159e-03")


def test_ratio():
    _test_format("kjashd_ratio_jkfndsjk", 0.3141, "0.314")


def test_temperature():
    _test_format("kjashd_temperature_jkfndsjk", 1273.15, "1273.2")


@pytest.mark.parametrize(
    "name",
    [
        "strain", "elongation", "draught", "spread"
    ]
)
def test_strains(name):
    _test_format(f"kjashd_{name}_jkfndsjk", 0.31416, "0.3142")


@pytest.mark.parametrize(
    "name",
    [
        "angle", "alpha"
    ]
)
def test_angles(name):
    _test_format(f"kjashd_{name}_jkfndsjk", np.pi / 2, "90.0")


def test_string():
    _test_format("", "str", "str")


@pytest.mark.parametrize(
    "type",
    [tuple, list, np.array]
)
def test_collections(type):
    _test_format("", type([1, 2, 3]), "1, 2, 3")


def test_disk_elements_false(monkeypatch):
    monkeypatch.setattr(Config, "PRINT_DISK_ELEMENTS", False)

    with pytest.raises(DoNotPrint):
        _test_format("disk_elements", [1, 2, 3], "")


def test_disk_elements_true(monkeypatch, tmp_path):
    monkeypatch.setattr(Config, "PRINT_DISK_ELEMENTS", True)

    with pytest.raises(DoNotPrint):
        _test_format("disk_elements", [], "")

    result = pyroll.report.plugin_manager.hook.property_format(value=[Transport()], name="disk_elements")
    assert "Transport" in result

    f = tmp_path / "result.html"
    f.write_text(result)

    webbrowser.open(f.as_uri())


def test_disk_elements_repr_mixin(tmp_path):
    result = pyroll.report.plugin_manager.hook.property_format(value=Transport(), name="")
    assert "Transport" in result

    f = tmp_path / "result.html"
    f.write_text(result)

    webbrowser.open(f.as_uri())


def test_disk_elements_shapely(tmp_path):
    result = pyroll.report.plugin_manager.hook.property_format(value=Point(0, 0).buffer(1), name="")

    f = tmp_path / "result.html"
    f.write_text(result)

    webbrowser.open(f.as_uri())


@pytest.mark.parametrize(
    "name",
    ["label", "points", "surface_x", "surface_y", "surface_z", "units"]
)
def test_guards(name):
    with pytest.raises(DoNotPrint):
        _test_format(name, "abc", "")


def test_geom_collection_guard():
    with pytest.raises(DoNotPrint):
        _test_format("", [Point(0, 0)], "")
