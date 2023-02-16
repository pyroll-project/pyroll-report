from typing import Collection

from shapely import Geometry

from ..pluggy import hookimpl
from .properties import DoNotPrint


@hookimpl(specname="property_format")
def do_not_print_units(name: str):
    if name == "units":
        raise DoNotPrint()


@hookimpl(specname="property_format")
def do_not_print_label(name: str):
    if name == "label":
        raise DoNotPrint()


@hookimpl(specname="property_format")
def do_not_print_points(name: str):
    if "points" in name:
        raise DoNotPrint()


@hookimpl(specname="property_format")
def do_not_print_geom_sequences(name: str, value: object):
    if isinstance(value, Collection) and not isinstance(value, str):
        for e in value:
            if isinstance(e, Geometry):
                raise DoNotPrint()
