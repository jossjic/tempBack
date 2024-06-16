"""
Python model 'test.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.14.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="Birth Rate", comp_type="Constant", comp_subtype="Normal")
def birth_rate():
    return 0.02


@component.add(
    name="Births",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "birth_rate": 1},
)
def births():
    return population() * birth_rate()


@component.add(name="Death Rate", comp_type="Constant", comp_subtype="Normal")
def death_rate():
    return 0.05


@component.add(
    name="Deaths",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "death_rate": 1},
)
def deaths():
    return population() * death_rate()


@component.add(
    name="Population",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population": 1},
    other_deps={
        "_integ_population": {"initial": {}, "step": {"births": 1, "deaths": 1}}
    },
)
def population():
    return _integ_population()


_integ_population = Integ(
    lambda: births() - deaths(), lambda: 2000000.0, "_integ_population"
)
